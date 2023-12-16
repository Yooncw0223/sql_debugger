
# SQL Debugger

This project serves as the final project submission for 6.5830 Database Systems for FA2023 (MIT). The team members are Brent Liu, Philip Li, and Chanwoo Yoon.

This project explores ways to create a tool to help debug potentially wrong SQL queries with as little user overhead as possible. Our main approach is to use a large language model (OpenAI-based) to understand what the user wants to extract from the database and propose various fixes. While syntax errors do arise in day-to-day uses, we do not focus on them since these problems mostly fall under the realm of LSPs/syntax/parsing (although LLMs do catch these errors). We focus on transferring the structural information of the database to the model so that it knows the correct attribute names.

The scripts can be run from the root location of this project using the command 'python3 -m ..FILE.. --PARAMETER=PARAM_VALUE'.

eval/ folder has scripts for model evaluations.
datasets/ folder has various jsonl and csv files that we used to fine tune our models. 
data_processing/ folder contains some of the scripts that we used to format the original dataset (.csv) into jsonl file format.

If any questions arise, please email chanwooy@mit.edu. I would be more than happy to answer! Thank you!
