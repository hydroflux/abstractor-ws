# abstractor-ws

## To Do List

### General To Do

- [ ] Create a fully built-out README
- [ ] Add watermark
- [ ] Duplicated results—add “multiple results” as an array to Document class in order to create more effective comments when encountering multiple documents
- [ ] When creating document instances, leave an indication if a book and page instance & a document number instance are on the same line (use the index) in order to create more effective comments
- [ ] In the same vein as the two above, create an indicator for any instances that are repeated (don't necessarily remove them)
- [ ] Figure out how to send cookies through to browser instances in order to get faster page load times
- [ ] Entire header should be created in the settings block, rather than relying on first & last recording dates in the dataframe
- [ ] Remove an additional space when dropping "see record" in order to cut the new line character out
- [ ] Consider an "append_text" function to go in general functions / file management which would strip, title case, & replace any unwanted information
- [ ] Compare parallel scripts from leopard & eagle in order to help refactoring
- [ ] Review all scripts for "standardized" functions that might be extrapolated
- [ ] Create a time_management file in settings to handle sleeps, dates, & timers
- [ ] Create a 'testing' script that imports all settings & variables & opens a browser instance so dev setup doesn't have to be completely manual
- [ ] Create a selenium general_functions script to handle duplicable functions that require the webdriver in order to run
- [ ] Create a "download_setup" series of functions where if download == yes: create_directory, get current files, change active directory, etc.
- [ ] Circle back to leopard download after completing the above
- [ ] Create a "big cat" repo to combine information that matches between tiger & leopard
- [ ] Add date / year into the document class in order to add the option to sort by date

### Leopard To Do

- [ ] Update multiple_documents comment to include actual document numbers and / or book & page numbers

### Tiger To Do

- [ ] Update multiple_documents comment to include actual document numbers and / or book & page numbers
- [ ] Re-design tiger to work with the code base for leopard
- [ ] Refactor login
- [ ] Create a logout script to work with tiger -- again based on leopard primarily
- [ ] Refactor environment to work with the new export, document_list, & execute functionality
- [ ] Refactor the execute script
- [ ] Refactor tiger search
- [ ] Refactor tiger open_document
- [ ] Refactor tiger record
- [ ] Refactor tiger download
- [ ] Update record (after refactoring) to work with multiple documents
- [ ] Document.number_results should be spread across open, record, & execute
- [ ] Create a convert_document_numbers script to work like leopard, but with the tiger document lists

### Eagle To Do

- [ ] For some reason the ’s isn’t catching on entries when the grantor has to hit show more, please review
- [ ] Update multiple_documents comment to include actual document numbers and / or book & page numbers
- [ ] Verify results after clicking into the document page
- [ ] Create a check that if there is anything in the “related” box, throw an extra nap in to make sure that the related documents are grabbed—this will also be an extra verification to make sure that all related documents are grabbed
- [ ] Add additional checks & balances for adding additional reception numbers (locating multiple documents)
- [ ] Auto generate hyperlinks—probably requires auditing the entire ‘reception_numbers’ page & doing a comparison against what’s in the document folder
- [ ] Add a semi-colon between the reporting of the success / failure of the document & remaining documents
- [ ] Create a check to add comments for multiple documents coming from the same line of the index—i.e. if book & page for a line item hits nothing, make sure the comment says to check the reception number document that comes through—alternatively, do it whether it hits or not
- [ ] Similar to the above line, create a check that ensures that if the book & page & the reception number document that returns is identical, the document is not duplicated on the run sheet
- [ ] Add “look for link text” to record—if the program is moving too fast it misses some links that don’t generate right away
- [ ] Implement 'medium_nap()'s when refreshing the page after encountering an exception
- [ ] Add a .strip() to Document class instance values when created in order to catch any numbers which were typed with extra space(s) on either side of the document value
- [ ] Count results doesn't work if the search button has never been pressed, add a fallback procedure to account for this--occurs when the browser instance is offscreen during a search
- [ ] If a grantor / grantee ends in a tag indicating more information is present, redo the search -- add to eagle record
- [ ] Create a convert_document_numbers script to work like leopard, but with the eagle document lists

### Crocodile To Do

- [ ] Create a new directory to work with the crocodile codebase
- [ ] Add all crocodile scripts (execute, login, logout, search, open, record, download)
- [ ] Integrate crocodile scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script

### Iguana To Do

- [ ] Create a new directory to work with the iguana codebase
- [ ] Add all iguana scripts (execute, login, logout, search, open, record, download)
- [ ] Integrate iguana scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script