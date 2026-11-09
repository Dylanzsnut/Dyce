# Logistics Delay Reason Classification Results

Classification pipeline results generated with Heuristic Pre-classification and Azure OpenAI Refinement.

| ID | Log Entry | Heuristic Category | Final Predicted Category | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Driver reported heavy traffic on highway due to construction | Traffic | **Traffic** | Confirmed |
| 2 | Package not accepted, customer unavailable at given time | Customer Issue | **Customer Issue** | Confirmed |
| 3 | Vehicle engine failed during route, replacement dispatched | Vehicle Issue | **Vehicle Issue** | Confirmed |
| 4 | Unexpected rainstorm delayed loading at warehouse | Weather | **Weather** | Confirmed |
| 5 | Sorting label missing, required manual barcode scan | Sorting/Labeling Error | **Sorting/Labeling Error** | Confirmed |
| 6 | Driver took a wrong turn and had to reroute | Human Error | **Human Error** | Confirmed |
| 7 | No issue reported, arrived on time | Other | **Other** | Confirmed |
| 8 | Address was incorrect, customer unreachable | Customer Issue | **Customer Issue** | Confirmed |
| 9 | System glitch during check-in at loading dock | Technical System Failure | **Technical System Failure** | Confirmed |
| 10 | Road accident caused a long halt near delivery point | Traffic | **Traffic** | Confirmed |