# Tech Stack Preferences

This project uses the following analytics platforms and tools. When providing code examples, recommendations, or technical guidance, prioritize these technologies:

### Analytics Platforms

**HEALIX (GCC Cloud Environment)**
- Platform: Databricks
- Languages: R and Python
- Available tools: STATA for statistical analysis

**MCDR (On-Premise Compute Cluster)**
- Platform: Cloudera Data Science Workbench (CDSW)
  - Languages: R and Python
  - Analytics Engine: Apache Spark
  - File System: Hadoop Distributed File System (HDFS)
- Platform: HUE for SQL-based data retrieval
- Available tools: STATA for statistical analysis

### Tool Specifications

- **Databricks**: Preferred for new analytics workflows in the cloud environment
- **CDSW**: Primary platform for on-premise Spark-based analytics with R/Python
- **HUE**: SQL interface for ad-hoc queries and data exploration
- **STATA**: Statistical analysis tool, especially for economics and econometrics research
- **Spark**: Main distributed computing engine for large-scale data processing
- **Hadoop/HDFS**: Underlying distributed storage system

### Guidance for Code Generation

When generating code or providing technical solutions:
1. Default to Python or R for analytics scripts
2. Leverage Spark for distributed data processing
3. Use SQL (via HUE) for straightforward data extraction
4. Reference STATA for econometric modeling and statistical analysis
5. Consider platform availability (HEALIX vs MCDR) when making recommendations
6. Prefer Databricks/HEALIX for new cloud-native workflows