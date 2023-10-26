# Project Name

Description of the project.

## Instructions

These instructions will guide you on how to run the code and perform the necessary steps.

### Prerequisites

- Python (version X.X.X)
- Required dependencies (mention if any)

### Installation

1. Clone the repository:

```shell
git clone <repository_url>
```

2. Install the required dependencies:
```shell
pip install -r requirements.txt
```

### Usage

1. Navigate to the project directory:
```shell
cd project-directory
```

2. Run the code:
```shell
python main.py [files]
```
Replace [files] with the names of the files to process, separated by a semicolon.

3. View the logs:
Logs will be saved in the logs directory with the format [filename]_[timestamp].log.

4. Output:
- The output will be saved as CSV files:
  - Individual files: [filename].csv 
  - Aggregated file: freguesias_aggregated.csv

### Example
```shell
python main.py file1.txt;file2.txt;file3.txt
```
This command will process file1.txt, file2.txt, and file3.txt.