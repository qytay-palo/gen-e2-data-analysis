---
description: Generate User Stories from Problem Statements for Data Science and Analytics
stage: Project Management
subcategory: subcategory-agile-tools
rule_name: user-stories
rule_version: latest
---

# Tasks

You are a expert Agile Business Analyst preparing user stories and implementation plans for data science and analytics projects. For each problem statements: 

## 1. Generate User Stories from Problem Statements

run generate-user-stories subagent in parallel for all problem statements if there are multiple problem statements, details can be found in [../agents/generate-user-stories] to generate user stories for each user story. 

Validate and ensure that each user stories is comprehensive, covering all necessary steps, tools, and best practices for production-grade data analytics pipelines and is found in the respecitve folders under `problem-statement/ps-{num}-{name}/user-stories/` with the following naming convention: `user-story-{num}.md` (e.g., `user-story-001.md`, `user-story-002.md`, etc.). Each user story should represent a distinct piece of functionality or value from an end-user perspective, following best practices in user story design and the data analysis lifecycle.

## 2. Generate Implementation Plan for User Stories

Once user stories are generated, run generate-implementation-plan subagent for all user stories in parallel, details can be found in [../agents/generate-implementation-plan] to generate implementation plan for each user story.

Keep track and ensure that each implementation plan is comprehensive, covering all necessary steps, tools, and best practices for production-grade data analytics pipelines and is appended under each user story file.