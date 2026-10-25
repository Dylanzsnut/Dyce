# Meeting Summary — Sample 02

**Source Transcript:** `sample_02_sprint_retrospective.txt`

### Executive Overview
- Sprint 14 completed 34 of 38 story points; slow CI/CD test pipelines blocked two spillover items. The team decided to optimize GitHub Actions by enabling Docker layer caching, sharding Playwright E2E tests, and separating smoke from full regression tests.

### Key Points
- API contract schema validation succeeded in catching three breaking payload changes prior to staging deployment.
- CI/CD pipeline duration had ballooned to 42 minutes per PR due to uncached Docker builds and sequential Playwright test execution.
- Sharding Playwright tests across 4 parallel workers combined with Docker Buildx registry caching is projected to reduce pipeline duration from 42 minutes to under 12 minutes with neutral runner cost impact.
- Flaky database time-zone tests caused four random pipeline failures during the sprint.

### Decisions Made
- Enable Docker Buildx registry layer caching and shard Playwright tests across 4 parallel workers starting in Sprint 15.
- Restrict PR-blocking pipelines to smoke E2E tests only, moving full regression suites to nightly scheduled runs on main.

### Action Items
- **Tomoko Sato**: Refactor flaky database time-zone tests to freeze UTC timestamps using freezegun *(Due: October 18)*
- **Priya Nair**: Tag 85 existing Playwright specs into @smoke versus @full-regression *(Due: October 19)*
- **Hoang Le**: Update GitHub Actions workflow YAML for Docker Buildx caching and 4-way Playwright sharding *(Due: October 20)*
- **Alex Rivera**: Track CI pipeline duration on the Sprint 15 dashboard against the sub-12-minute target *(Due: Ongoing / Sprint 15)*
