# Abstractor

Automating the process of searching for government records on bulky, difficult to access websites.

## Table Of Contents

- General Information
- Video
- Features
- Example Output
- Status
- Technologies
- Contact

## General Information

- Simplifies the process of creating chain of title, locating property, searching individual names, and downloading & hyperlinking document images.
- Automates mouseclicks and search functionality in order to remove the possibility for mistyping or "fat-fingering" when searching for documents
- Removes wait times for the user, so that if a website is slow or unresponsive, the burden of time is taken away from the user and placed on the program
- Creates uniform, consistent output that can be relied on and used for further research and deeper insights
- Removes the time cost and burden of continual data entry, so that hitorical data professionals can focus on what they're best at

## Video

- [Abstractor Example Video](https://youtu.be/lkM0ldEOoPI)

## Features

- On a county-by-county basis, takes inputs of either a "Name", "Reception Numbers" / "File Numbers", or "Book" / "Volume" / "Page" numbers
  - A "Name" search will take search a name given by the use as an input
  - "Reception Number" / "File Number" and "Book" / "Volume" / "Page" searches use take a given file path and XLSX file name, importing the documents to be searched into a list that is looped over until completion
- Retrieves information located on county websites by searching given inputs and recording the information located at each search point
- Creates an XLSX file as an output, formatted based on client designations
- When "Download" is selected as an option,
  - Creates a "Document Directory" titled "Documents"
  - Downloads and renames document images based on context provided by the user, saved to the "Document Directory"
  - Creates relative hyperlinks for each document image downloaded, connected to the "Document Directory"
  - Creates a "Hyperlink" tab in the final output XLSX file, with hyperlinks to each document image in the directory (**example video shows "Direct Links" which are created on record)
- Creates specialized comments for any search point that does not return expected results, which conditionally format their respective line items for easy identification
  - Identifies when "No Record Can Be Found" at a specific search point
  - Checks for "Multiple Documents" located at a single search point (recording each document and leaving appropriate comments for each)
  - Checks for "No Image Found" at any givenn document when "Download" is selected as an option, whether "Multiple Documents" are found or not
- Creates a "Limitations" output based on the county / state searched and client specifications
- Prints output with a "Last Updated" date listed at the bottom of the XLSX document

## Example Output

[Example Output](https://user-images.githubusercontent.com/73364397/135174462-d786d3a0-91ad-4d75-97fa-9389ab78bf51.png)

## Status

- In production, continually updating based on contracts received.

## Technologies

- Python 3.9.2
- Selenium Version 3.141
- Chromedriver (Version Updated on Runtime)

## Contact

- Jack Hubert
  - [LinkedIn](https://www.linkedin.com/in/jackhubert/)
  - [GitHub](https://github.com/hydroflux)
