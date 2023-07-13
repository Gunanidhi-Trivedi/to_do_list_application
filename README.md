# to_do_list_application


## Local_setup ################################################

### Creating virtual environment  
- `python -m venv .env`
### Activate the virtual environment 
- `.env\Scripts\activate`

### Install all the required packages
- `pip inatall -r requirements1.txt`
#### note -  requirements.txt file is used for deployment in render


### Start the server
- `python main.py`


## Folder Structure ################################################

- `static` - default `static` files folder. It serves at '/static' path.
- `static/style.css` Custom CSS.
- `templates` - Default flask templates folder
- `instance/database.sqlite3` - sqlite database file 
- `documentation` - project documentation file
- `main.py` - main code file
- `requirements.txt` - contain all the required module dependencies for local setup
- `requirements1.txt` - contain all the required module dependencies for hosing in render

```

├── instance 
    └── database.sqlite3
├── main.py
├── documentation.pdf
├── readme.md
├── requirements.txt
├── requirements1.txt
├── static
│   └── style.css
└── templates
    ├── add_task.html
    ├── base.html
    ├── edit_task.html
    ├── home.html
    ├── login.html
    └── sign_up.html
    
```
