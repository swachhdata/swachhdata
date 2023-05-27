![](https://raw.githubusercontent.com/Swachhdata/Swachhdata/main/logo/sd-cover.png)

# Swachhdata

Swachhdata is an open-source Python package that offers simple and efficient tools for cleaning and transforming text data. It aims to provide accessibility to everyone and encourages reusability in various contexts. With Swachhdata, you can easily clean and preprocess your data using a collection of functions and build pipelines to streamline your data processing tasks. 

[![PyPI version](https://badge.fury.io/py/swachhdata.svg)](https://badge.fury.io/py/swachhdata)
[![CodeFactor](https://www.codefactor.io/repository/github/Swachhdata/Swachhdata/badge)](https://www.codefactor.io/repository/github/Swachhdata/Swachhdata)
[![Downloads](https://static.pepy.tech/personalized-badge/Swachhdata?period=total&units=international_system&left_color=gray&right_color=blue&left_text=Downloads)](https://pepy.tech/project/Swachhdata)
![GitHub last commit](https://img.shields.io/github/last-commit/Swachhdata/Swachhdata?color=green)
[![GitHub](https://img.shields.io/github/license/Swachhdata/Swachhdata.svg)](https://github.com/Swachhdata/Swachhdata/blob/master/LICENSE)



## Key Features

- **Data Cleaning**: Swachhdata provides a comprehensive set of functions to clean and sanitize your text data. Whether you need to remove stopwords, perform lemmatization, or do tokenisation, Swachhdata has you covered.

- **Flexible Input**: Swachhdata supports various data types, including strings, lists of strings, Pandas DataFrames, Pandas Series, and NumPy arrays. You can seamlessly input your data into the functions or pipelines without worrying about the format.

- **Pipelines**: You can create data processing pipelines by chaining multiple functions together. This allows you to perform a series of transformations on your data with a single command, making your workflow more efficient.

- **Automatic Data Type Detection**: Swachhdata intelligently detects the data type of your input, allowing you to use appropriate cleaning methods automatically. This feature eliminates the need for manual conversions and saves you valuable time.

- **Multiple Backend Engines**: Swachhdata provides convenient wrapper functions for performing tasks such as lemmatization and stemming on your text data. These functions allow you to choose the background engine between NLTK, SpaCy, and Gensim, giving you flexibility in selecting the most suitable option for your specific requirements.

- **Open Source and Commercially Usable**: Swachhdata is released under the MPL-2.0 license, making it open source and commercially usable. You can freely use, modify, and distribute the package in your projects, whether they are personal, academic, or commercial.


## Installation

You can install swachhdata using pip:

```
pip install swachhdata
```

## Usage

To use Swachhdata, import the package in your Python script or Jupyter Notebook:

```python
import swachhdata.text as sdt
```

Once imported, you can start utilizing the functions and pipelines provided by Swachhdata to clean and transform your data. Here's an example of how you can remove duplicates from a list of strings using Swachhdata:

```python
pipeline = sdt.htmlRecast() + \
           sdt.EscapeSequencesRecast() + \
           sdt.MentionsRecast(process='remove') + \
           sdt.ContractionsRecast() + \
           sdt.CaseRecast(process='lower') + \
           sdt.EmojiRecast(process='replace', space_out=True) + \
           sdt.HashtagsRecast(process='remove') + \
           sdt.ShortWordsRecast(min_length=3) + \
           sdt.StopWordsRecast(package='nltk') + \
           sdt.NumbersRecast(process='replace', seperator=',') + \
           sdt.AlphabetRecast(process='all') + \
           sdt.PunctuationsRecast() + \
           sdt.LemmatizationRecast()

pipeline.setup(text)
text = pipeline.recast()
```


For more detailed examples and documentation, please refer to the [Documentation](https://swachhdata.readthedocs.io/en/latest/).

## Contributing

Swachhdata welcomes contributions from the open-source community. If you encounter any issues, have ideas for improvements, or would like to add new features, please submit a pull request on the [GitHub repository](https://github.com/Swachhdata/Swachhdata).

Before submitting a pull request, please ensure that your code adheres to the project's coding conventions and is thoroughly tested.

## License

Swachhdata is released under the MPL-2.0 license. For more information, please refer to the [LICENSE](https://github.com/Swachhdata/Swachhdata/blob/main/LICENSE) file.

## Contact

If you have any questions, suggestions, or feedback, you can reach out to the Swachhdata team by [opening an issue](https://github.com/your-username/Swachhdata/issues) on the GitHub repository.

---

Thank you for choosing Swachhdata! We hope you find it helpful in cleaning and transforming your data.

## Documentation- 

* https://Swachhdata.readthedocs.io/en/latest/ (Update coming soon!)
* [Examples](https://colab.research.google.com/drive/1IH7ve5xoQ4vLyrRP4HvTCYBlj1Ub1GGS?usp=sharing#scrollTo=3Seymy37xQk4)

## Author-

<a href="https://www.kritikseth.com/redirect" target="_parent"><img src="https://raw.githack.com/kritikseth/kritikseth/master/redirect.svg" alt="Kritik Seth"/></a>
