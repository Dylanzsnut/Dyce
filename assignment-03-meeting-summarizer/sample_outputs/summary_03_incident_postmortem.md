# Meeting Summary — Sample 03

**Source Transcript:** `sample_03_incident_postmortem.txt`

### Executive Overview
- A blameless post-mortem was held for a SEV-2 checkout latency incident on October 14 that affected 1,420 checkout attempts. Root cause was PostgreSQL connection pool exhaustion triggered by automatic pod scaling during a flash sale; preventative fixes include deploying PgBouncer and reducing application pool sizes.

### Key Points
- 1,420 checkout attempts timed out (>15s) and 68 support tickets were opened; idempotency keys prevented any duplicate charges.
- The payment-webhook-worker scaled from 4 to 20 pods during flash traffic, each opening 25 DB connections (500 total), exceeding PostgreSQL's 450 max_connections ceiling and starving checkout API queries.
- Manually capping replicas to 10 pods dropped connections to 260 and normalized p99 latency to 180ms within 5 minutes.
- Current database connection alerts at 95% fired too late to avert degradation.

### Decisions Made
- Deploy PgBouncer in transaction-pooling mode in front of the payments PostgreSQL cluster.
- Reduce payment-webhook-worker SQLAlchemy connection pool size from 25 to 8 per pod.
- Lower the database connection alert threshold to 75% utilization sustained over 2 minutes.

### Action Items
- **Tuan Pham**: Deploy reduced SQLAlchemy pool size (pool_size=8) to production after staging soak testing *(Due: October 15)*
- **Elena Rostova**: Configure 75% connection utilization threshold alert in Grafana and Alertmanager *(Due: October 16)*
- **Nina Patel**: Send apology vouchers to the 68 affected customer ticket holders *(Due: October 16 at 12:00 PM)*
- **Marcus Vance**: Provision PgBouncer in staging *(Due: October 20)* and execute production cutover *(Due: October 24)*
