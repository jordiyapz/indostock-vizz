# IndoStock Vizz

This project is a final project for Data Visualization course at Telkom University. 

You can find the working app here: https://indostock-vizz.herokuapp.com/app

Thanks.

# Installation

1. Create virtual environment: `python3 -m venv env`

2. Activate the virtual environment:

```
  # Windows
  > ./env/Scripts/activate.bat

  # Linux
  > source env/bin/activate
```

3. Run: `pip install -r requirements.txt`

4. Run: `pip install -e .`

5. Run: `bokeh serve app`

6. Download the dataset:

```
  # Linux
  > gdown --id 1Hb9K3EyJ1VyX_NCFKik6l-GJPuruJ_cL -O downloads/indonesia-stocks.zip
  > unzip -o downloads/indonesia-stocks.zip -d app/data
```

> Note on Windows: 
> 1. Run: `gdown --id 1Hb9K3EyJ1VyX_NCFKik6l-GJPuruJ_cL -O downloads/indonesia-stocks.zip`
> 2. Manually unzip the `indonesia-stock.zip` from `downloads` to directory `app/data`.

7. Open http://localhost:5006/app
