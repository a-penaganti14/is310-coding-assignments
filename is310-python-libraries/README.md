# College Sports Spending Data Entry

This project collects school-level college athletics spending records. Each record includes a school, year, spending category, amount in USD and source. These fields fit our IS310 group topic, the business of college sports. The three example schools are real Big Ten universities (Illinois, Michigan and Ohio State). The sample entries use verified 2024 total athletic expenses from the Knight-Newhouse College Athletics Database. These are total athletic operating expenses, including athletic scholarship costs, in current dollars. All three entries use the same year and category for a fair comparison.

## Data sources

2024 total athletic expenses, current dollars:

- University of Illinois Urbana-Champaign: $169,474,512. [Knight-Newhouse](https://www.knightnewhousedata.org/fbs/big-ten/university-illinois-urbana-champaign)
- University of Michigan: $241,856,430. [Knight-Newhouse](https://www.knightnewhousedata.org/fbs/big-ten/university-michigan)
- Ohio State University: $295,174,868. [Knight-Newhouse](https://www.knightnewhousedata.org/fbs/big-ten/ohio-state-university)

## Python setup and running the CLI

From the `is310-coding-assignments` repository root on macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r python-libraries/requirements.txt
python python-libraries/cli_data_entry.py
```

On Windows PowerShell, create the environment with `python -m venv .venv`, activate with `.\.venv\Scripts\Activate.ps1` and run the same install and script commands. Add `.venv/` to your repository's `.gitignore`.

The CLI displays example records, requests at least two new records, validates each field and shows each entry for confirmation. An incorrect entry gets re-entered. Only confirmed entries are written to `python-libraries/college_sports_spending.json`. Later runs append confirmed entries to the existing JSON list. The terminal prints the full output path.

## Running the HTML version

Open `python-libraries/index.html` in a browser. Fill out the fields, review each record, then click **Confirm record**. After confirming at least two records, click **Download JSON**. The HTML version downloads a JSON file from the browser and does not automatically write to the repository folder.

## Interface comparison

The Python interface works well for people who are comfortable entering data in a terminal. Its confirmation loop keeps the workflow straightforward, but entering fields one by one makes reviewing a large number of records slower. The HTML interface shows all the fields at once and uses a dropdown for categories, which makes the choices clearer. Its review screen also makes mistakes easier to spot. Both versions require a school, year, category, amount and source. The terminal version accepts any nonempty category, while the browser suggests common categories in a dropdown. The CLI saves directly to a local file, whereas the browser provides a download.

For classmates with little coding experience, I would choose the HTML version. For a researcher who already works in a terminal, the Python version is simpler to include in a local data workflow.

## AI development record

AI helped me with the writing of the readme file and also helped me when I was confused with the Python. It also helped me write some of the html files when I was a little confused.

## Contents

- `cli_data_entry.py`: Rich-powered data-entry script
- `index.html`: equivalent browser interface
- `requirements.txt`: Python dependency
- `college_sports_spending.json`: three Big Ten schools with verified 2024 total athletic expenses and source URLs
- `ai-chat-log.md`: development assistance record

## Peer testing

Peer testing is a separate step after posting your repository link. Test a classmate's interface, enter two records, attach its output and give specific feedback in their GitHub discussion thread. 
