# BACKLOG

## General To Do

- [ ] Handle 'Document Date' added to the abstract_dictionary across all recording scripts--maybe make a new utility settings script which handles 'Document Date'
- [ ] Create a breakdown of adding a new county ('skeleton structures', 'general_functions', etc.)
- [ ] Change 'file_management' to 'dataframe_management' & split out functions into multiple utility scripts
- [ ] Create directory for objects & split abstract_objects into separate scripts
- [ ] Create a fully built-out README
- [ ] Add watermark
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
- [ ] Create a double-check option for eagle--possibly under the "review" as a switch in order to check for any related documents missing
- [ ] Best order of operations for file management should be to create the folder first & then put the documents folder inside of it, rather than bundling at the end
- [ ] I keep returning the reception number as a way to 'get' the document number--but if it matches (or if it can be stored a different way), this is completely redundant
- [ ] Add program_type to  the 'started on...' line when starting a program (checks for cases where the wrong program type was chosen & logging in is time extensive)
- [ ] Document number & document_image_available should be part of the document class--in addition to this, "download" could be an attribute of the document that is added when the document list is imported, & gets turned off if the document image isn't available
- [ ] Create a class for the "abstraction" itself in order to avoid passing so many variables around between functions--would really clean up the code & make it easier to interact with documents when the code breaks
- [ ] Add county to the document class as well to avoid passing county around to different functions
- [ ] If websites & logins are added to the county class the open_site function can be generalized across all scripts
- [ ] Add a check to the environment file to make sure that the county information is entered correctly before starting the webdriver
- [ ] If continuing to use the 'extrapolate_document_value' function with name_search, function & it's spin-offs should be renamed accordingly (criteria, value, etc.)
- [ ] Demo prompts should have a "go back" option
- [ ] There is a function in export_settings to create the full_disclaimer---ideally there should be no functions in settings files
- [ ] Change "Document Found" so that it lists either "recorded" or "recorded & downloaded" instead of located
- [ ] Look into github vulnerability link that's broken
- [ ] Convert notes from demo into a proper README
- [ ] Separate imports for each file based on source location (settings, main directory, outside imports, etc.)
- [ ] Add input() to every timeout which doesn't have a natural resolution in order to pause the program at each exception (& create a correction)
- [ ] Consider creating an error_handling function for exceptions which takes a screenshot & throws an input together with the above suggestion

### Imports To Do

- [ ] Allow user to review the imported excel document & choose the column / columns to run
- [ ] Add download flag to document class & set at import in order to avoid passing the flag around
- [ ] When creating document instances, leave an indication if a book and page instance & a document number instance are on the same line (use the index) in order to create more effective comments---set up for Document class just needs to be implemented
- [ ] If 0 documents are imported, close the program and send a message
- [ ] If download is true and the document is already located in the target document directory, add a medium nap for eagle--in order to do so, add "downloaded" or something similar to the Document class for imports

### Exports To Do

- [ ] Add hyperlinks before exporting (working on now)

### Leopard To Do

- [ ] Update multiple_documents comment to include actual document numbers and / or book & page numbers
- [ ] HIGH PRIORITY -- refactor leopard execute
- [ ] move "get_reception_number" around into download document--passing around 'document_number' is redundant & the document can't be downloaded unless it's on the page anyway
- [ ] Remove anything with the "stock download" name before clicking the download button--avoid creating an issue with crash / restart
- [ ] Update scripts with new general functions (i.e. assert_window_title)
- [ ] Update the record function to set the reception number rather than return it

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
- [ ] Create a "download only" option for execution
- [ ] Update scripts with new general functions (i.e. assert_window_title)
- [ ] Update the record function to set the reception number rather than return it

### Eagle To Do

- [ ] Update multiple_documents comment to include actual document numbers and / or book & page numbers
- [ ] Verify results after clicking into the document page
- [ ] Auto generate hyperlinks—probably requires auditing the entire ‘reception_numbers’ page & doing a comparison against what’s in the document folder
- [ ] Create a check to add comments for multiple documents coming from the same line of the index—i.e. if book & page for a line item hits nothing, make sure the comment says to check the reception number document that comes through—alternatively, do it whether it hits or not
- [ ] Similar to the above line, create a check that ensures that if the book & page & the reception number document that returns is identical, the document is not duplicated on the run sheet
- [ ] Implement 'medium_nap()'s when refreshing the page after encountering an exception
- [ ] Add a .strip() to Document class instance values when created in order to catch any numbers which were typed with extra space(s) on either side of the document value
- [ ] Create a "download only" option for execution
- [ ] Update scripts with new general functions (i.e. assert_window_title)
- [ ] Update the record function to set the reception number rather than return it
- [ ] Move the logic for next result / previous result into its own script
- [ ] Eagle browser can't handle x requests in y time period---perform tests across multiple computers (& more specifically IP addresses) in order to determine whether its the IP or the user account that is overworking the server
- [ ] Clean up download_document--switch to download, get the frame switches together under a single function, & handle number of documents & stock download separately
- [ ] In addition to above, no need to even look at the download if it's been previously downloaded

### Crocodile To Do

- [ ] Integrate crocodile scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script ??? need to see what an index looks like
- [ ] Create an "review", & "download only" option for execution
- [ ] Need to create an application path for multiple results
- [ ] Create a fallback procedure to check for logout in order to log back in
- [ ] Test against as many document types as possible--documents don't appear to be consistent across different doc types
- [ ] Initial open_search needs a delay or additional check--first reception number doesn't appear (likely will occur again)
- [ ] Continuing above, the best case scenario may be to check the text field for the reception number & see if it matches the information attempted to be entered
- [ ] Crocodile should probably be changed to alligator
- [ ] Create a function similar to the 'get_reception_number' function for matching book / page numbers in crocodile open_document
- [ ] While working with multiple documents, figure out a way to store multiple document links with each result
- [ ] Look into external link issue--shouldn't be opening a new window
- [ ] Consolidate the different functions wrapping around crocodile open_document (probably create ~ 2 higher order functions for handling / verifying the results)
- [ ] Refactor crocodile record---probably into a check_index function and an aggregate function
- [ ] Name search currently only works with a "first name" / "last name" split--needs to be more robust to work in multiple scenarios

### Buffalo To Do

- [ ] Add all buffalo scripts (execute, record, download)
- [ ] Integrate buffalo scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution
- [ ] Update buffalo error_handling with use cases -- currently has none

### Armadillo To Do

- [ ] Audit armadillo reception numbers to match index numbers input
- [ ] Integrate armadillo scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution

### Iguana To Do

- [ ] Create a new directory to work with the iguana codebase
- [ ] Add all iguana scripts (execute, login, logout, search, open, record, download)
- [ ] Integrate iguana scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution

### Dolphin To Do

- [ ] Create a new directory to work with the dolphin codebase
- [ ] Add all dolphin scripts (execute, login, logout, search, open, record, download)
- [ ] Integrate dolphin scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution