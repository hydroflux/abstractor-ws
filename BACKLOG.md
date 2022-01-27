# BACKLOG

## General To Do

- [ ] Create a 'timers' script (pull from 'file_management' and 'general_functions') or otherwise a 'time_management' script to handle sleeps, dates, timers, etc.
- [ ] Comment imports and section by type
- [ ] In the same vein as the two above, create an indicator for any instances that are repeated (don't necessarily remove them)
- [ ] Figure out how to send cookies through to browser instances in order to get faster page load times
- [ ] Consider an "append_text" function to go in general functions / file management which would strip, title case, & replace any unwanted information
- [ ] Review all scripts for "standardized" functions that might be extrapolated
- [ ] Create a "big cat" repo to combine information that matches between tiger & leopard
- [ ] Create 'master' scripts after breaking out directory scripts into smaller pieces--i.e. 'login' can be a 'master' script; 'fill_search_field' & the like can be built out further as well; 'execution' as well
- [ ] Exception review could include a 'continue?' option that could close out the browser
- [ ] Replace all 'scroll' functions with 'center element'
- [ ] Eliminate iframe_handling script?
- [ ] Update & uncomment the the 'execute_demo' function in the 'environment' file
- [ ] If performing a 'refresh' loop, only allow for x # of refreshes before pausing for input--don't want to create too many requests (create a Document class attribute?)
- [ ] Determine the best place to place the 'check_length' function for all scripts

## Classes To Do

- [ ] Create a 'Directory' class with two attributes--"files" and "number_files"
- [ ] The 'target_directory' and 'document_directory' attributes on the Abstract class can be instances of the Directory class
- [ ] Drop the 'document_directory_files' attribute from the Abstract class

### Abstract Class To Do

- [ ] Add 'transform' to abstract initialization dependent on the county
- [ ] Update either the 'Abstract' or 'Project' class to handle whether to export & bundle a project, rather than having the argument inline of the 'execute_program' functions (across directories)
- [ ] Add instance functions to add either 'empty' or 'n/a' values to the dataframe, using 'self', some flag trigger, and a string value of the dataframe column to be affected

### County Class To Do

- [ ] If websites & logins are added to the county class the open_site function can be generalized across all scripts
- [ ] The above can also be used for the 'Program' class instead

### Document Class To Do

- [ ] Update 'document.value' to 'document.search_value' to create a better differentiation between 'document.reception_number'???
- [ ] Turn off 'download' flag if document image is not available?--could be a better solution to checking image available before trying to download
- [ ] Add date / year into the document class in order to add the option to sort by date
- [ ] Consolidate the 'value' attribute and the 'document_value' instance function--too confusing and creating problems
- [ ] Create class functions for 'document_found', 'document_downloaded', 'no_document_found' and 'no_document_downloaded' using the functions from the 'file_management' script
- [ ] Set the 'image_available' attribute automatically True, to be turned to 'false' if otherwise noted
- [ ] Add an 'is_duplicate' attribute to the Document class, set using 'download_management' (or otherwise the 'previously_downloaded' function) and called in the printout statements

### Program Class To Do

- [ ] Create a 'Program' class
- [ ] Use the 'Program' class to create a united 'execute' function across multiple directories

### Project Class To Do

- [ ] Update either the 'Abstract' or 'Project' class to handle whether to export & bundle a project, rather than having the argument inline of the 'execute_program' functions (across directories)

## Program To Do

- [ ] Create a 'closure' script (or named something similar) to handle exporting the document, bundling the project, and closing the browser (and potentially handling a 'logout' function)

### Runtime To Do

- [ ] Add program_type to the 'started on...' line when starting a program (checks for cases where the wrong program type was chosen & logging in is time extensive)
- [ ] Add a comment indicating how many documents have been completed
- [ ] Update parameter (and then argument) order for all instances of 'document_found' and 'no_document_found'
- [ ] Add a check to the environment file to make sure that the county information is entered correctly before starting the webdriver
- [ ] Create log files on run returning various metrics => create a comment function that takes a comment as an argument and then updates an object to be exported & prints to the screen
- [ ] Move the webdriver creation up from all 'execute' files into the 'environment' script and pass into the execute functions as an argument

## Project Management To Do

### Conditional Formatting To Do

- [ ] Up-To-Date

### Content To Do

- [ ] Up-To-Date

### Defunct Hyperlink To Do

- [ ] Integrate unused functions into the 'hyperlinks' script
- [ ] Delete the 'defunct_hyperlink' script

### Export To Do

- [ ] Create an 'export' subdirectory inside project management (come up with a better name)
- [ ] If nothing is recorded, do not create a base runsheet or a folder
- [ ] Add hyperlinks not if 'download' flag is true on abstract, but rather if a document_directory exists--maybe check length of the document_directory for files with the county prefix
- [ ] Add volume & document date (effective date for now) to the dataframe at outset, then remove for each county not needed in "transform"
- [ ] Update date formatting to named months input at the beginning
- [ ] Consider throwing a trigger requesting the dates
- [ ] If there is a file matching the created file (i.e. xxxx-Base-Runsheet) which exists, pause and get input to see what the user wants to do
- [ ] Automatically export a 'color coding legend' for all documents as an additional tab
- [ ] Add watermark
- [ ] Add a print statement at the end to indicate what type of run sheet was created (& the section)
- [ ] If a base runsheet folder has already been created, create a new one

### Font Formats To Do

- [ ] Up-To-Date

### Generate Document List To Do

- [ ] Allow user to review the imported excel document & choose the column / columns to run
- [ ] Add download flag to document class & set at import in order to avoid passing the flag around
- [ ] When creating document instances, leave an indication if a book and page instance & a document number instance are on the same line (use the index) in order to create more effective comments---set up for Document class just needs to be implemented
- [ ] If 0 documents are imported, close the program and send a message
- [ ] If download is true and the document is already located in the target document directory, add a medium nap for eagle--in order to do so, add "downloaded" or something similar to the Document class for imports
- [ ] Armadillo, leopard & tiger use convert_document_numbers, maybe make a workspace level script that checks counties against individual 'convert_document_numbers'
- [ ] Update 'display_document_list' to show all available attributes attached to a document
- [ ] Entire header should be created in the settings block, rather than relying on first & last recording dates in the dataframe
- [ ] Compare parallel scripts from leopard & eagle in order to help refactoring

### Hyperlinks To Do

- [ ] Integrate useful functions from the 'defunct_hyperlinks' script into the 'hyperlinks' script
- [ ] Determine a way to add hyperlinks into the xlsx document prior to export instead of creating a separate sheet--try using some kind of 'replacement' function, or otherwise avoid writing the 'Reception Number' column until the hyperlinks can be created

### User Prompts To Do

- [ ] Demo prompts should have a "go back" option

## Selenium Utilities To Do

### Element Interaction To Do

- [ ] Up-To-Date

### Inputs To Do

- [ ] Add an option before clicking a button to allow for scrolling to 'top', 'bottom', or 'centering'--instead of automatically centering the element

### Locators To Do

- [ ] Consider adding an option / flag (or even a standalone function which accepts a locator as an argument) to simply return True / False if only waiting for the element to load, rather than looking for the element itself---could use in both tiger and leopard 'record' scripts when dealing with the document image

### Open To Do

- [ ] Up-To-Date

## Settings To Do

### Assets To Do

- [ ] Up-To-Date

### County Variables To Do

- [ ] Eliminate superfluous lines of code commented out at previous testing stages across all scripts
- [ ] Check all variables in each 'county_variables' script to make sure they are still being used
- [ ] Streamline variable names across all 'county_variables' scripts
- [ ] Create class variables on the Document class for any 'county_variables' used across multiple / all scripts

### Objects To Do

- [ ] Up-To-Date

### Download Management To Do

- [ ] Consolidate the prepare, & check functions in download management--had a case where a 500+ page document was clicked & downloaded properly, but 173 in update, 145 in rename, & 140 in prepare raised a value error that it wasn't a file, even though circling back indicated that it was downloaded properly, and with the expected name
- [ ] Along with above, the new function for waiting for a download & then renaming it could probably be worked together in a new logic path
- [ ] The 'document_directory' should be created if 'download' is true but not otherwise
- [ ] Check if 'document_directory' (.exists?) each time a document is downloaded, & create otherwise
- [ ] Search both the 'download_name' (is that the correct attribute) and the 'new_name' when determining if a document has been downloaded or not (previously_downloaded)
- [ ] Create some series of checks (maybe in 'transform' scripts) to check for previously downloaded documents at the outset--just have to be careful about documents with multiple results (but that could probably be handled with the 'number_results' attribute
- [ ] Move the 'document_downloaded' / 'no_download' logic from the 'download' scripts into the 'previously_downloaded' and 'update_download' functions
- [ ] Streamline the functions involved in the 'download_management' script--they're kind of a mess
- [ ] Work a conditional back into 'update_download'---there's no conditional, so 'no_download' function will never be thrown
- [ ] 'is_duplicate' function needs a route for Document types other than 'document_number' for updating the name of the download
- [ ] 'is_duplicate' and 'previously_downloaded' functions should be added onto the Abstract(?) class
- [ ] Create a print statement for if a document is a duplicate and therefore will have a new reception number / download name
- [ ] Create a print statement to identify if a document has already been downloaded and is therefore has been 'previously_downloaded'
- [ ] 'prepare_for_download' function could be extrapolated to a certain point--creating the document directory and getting the number of directory files could be a generalized function (probably on ad Directory class), just need to determine what to do about other 'preparation' steps
- [ ] Change directory into the document directory during 'prepare_for_download'???
- [ ] Ideally, the only script specific 'download' function would be the 'execute_download' function

### Driver To Do

- [ ] Up-To-Date

### Error Handling To Do

- [ ] Consider creating an error_handling function for exceptions which takes a screenshot & throws an input together with the above suggestion
- [ ] Add input() to every timeout which doesn't have a natural resolution in order to pause the program at each exception (& create a correction)--maybe something to follow up 'extrapolate_document_value', like 'input(, please review.\nPlease press enter after reviewing error)' + a screenshot

### File Management To Do

- [ ] Consolidate 'split_book_and_page' and 'split_volume_and_page' functions
- [ ] Change "Document Found" so that it lists either "recorded" or "recorded & downloaded" instead of located
- [ ] Change 'file_management' to 'dataframe_management' & split out functions into multiple utility scripts
- [ ] Best order of operations for file management should be to create the folder first & then put the documents folder inside of it, rather than bundling at the end

### General Functions To Do

- [ ] Up-To-Date

### iFrame Handling To Do

- [ ] Integrate 'iframe_handling' into 'selenium_utilities' directory

### Initialization To Do

- [ ] Up-To-Date

### Invalid To Do

- [ ] Integrate appropriate functions from other scripts into the more generalized 'invalid' script, which has replaced the 'bad_search' script
- [ ] Create sub-functions for recording 'invalid' or 'bad' values which can be extrapolated to all working engine scripts
- [ ] Create a better suited method of using the 'no_document_image' function--currently used in 'armadillo', 'rattlesnake' and 'leopard'
- [ ] Determine if any other switches need to be put in place for the 'record_invalid_search' function if the abstract program type is 'review' or 'download_only'--further, this function may do well handling additional program logic overall

### PDF Merger To Do

- [ ] Update PDF merger to work on a county by county basis
- [ ] Handle cases where a '-1' document is valid
- [ ] Consider creating an independent program for the pdf_merger

## County Programs To Do

### Armadillo To Do

- [ ] Create a "download only" option for execution
- [ ] Create a final prompt before logging out & closing the browser in order to review documents IF PAID & checkout
- [ ] Create some consistency between 'document.reception_number' & 'document.value' in order to avoid constantly updating
- [ ] Update the validation file with the proper use of 'verify' & 'validate' (definitions have been added)
- [ ] Delete 'record' comment block accessing document tables after 09/17 (assuming active testing is done in the meantime)
- [ ] Get clarification around 'Document Date' vs. 'Effective Date' for formatting
- [ ] Get clarification around 'Book' vs. 'Volume' for formatting
- [ ] Create a 'no results' handler
- [ ] Add 'start_time' as an optional argument for document found depending on download state
- [ ] Update validation & verification functions to a similar structure used for rattlesnake
- [ ] Refactor 'record' functions, in particular the way that the validation is being handled
- [ ] Refactor 'open_document' selenium functions into selenium utilities directory
- [ ] Refactor 'record' selenium functions into selenium utilities directory
- [ ] "next" page could work effectively for recording armadillo documents with multiple results, & would cut down on search time
- [ ] Create a way to handle multiple documents being returned but not all being validated in the "Multiple documents" comment
- [ ] Use 'document_description' to determine if the 'next' document is a duplicate
- [ ] Perform a substring replacement for " 's " and other monikers
- [ ] Include 'year' in search in order to refine 'multiple results'
- [ ] Grab document_descriptions links to speed up the process of searching for multiple results
- [ ] If downloads are 'paid' then login isn't necessary--and will break the site application; update accordingly
- [ ] Consider 'checking for subscription'??? <--- could be added to eagle as well
- [ ] Options should be created in the environment file, the 'use_prompts' file, or a new file specifically for handling options
- [ ] Refactor 'record' script into its own directory
- [ ] Consider lengthening grantor / grantee fields for armadillo
- [ ] Update all scripts to work with the 'Project' and 'Abstract' classes

### Buffalo To Do

- [ ] Add all buffalo scripts (execute, record, download)
- [ ] Integrate buffalo scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution
- [ ] Update buffalo error_handling with use cases -- currently has none
- [ ] Update all scripts to work with the 'Project' and 'Abstract' classes

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
- [ ] Add 'download' decision to Document class & document instances
- [ ] Add 'start_time' as an optional argument for document found depending on download state
- [ ] IF not download OR if previously downloaded, add a couple of seconds--thats where I'm losing related documents

### Dolphin To Do

- [ ] Create a new directory to work with the dolphin codebase
- [ ] Add all dolphin scripts (execute, login, logout, search, open, record, download)
- [ ] Integrate dolphin scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution

### Eagle To Do

- [ ] Create a transform list function to handle hyphenated numbers coming from specific reports
- [ ] Change download so that it checks before searching if only downloading need to search, then validate the number of search results,  THEN check to see if it's been downloaded or not
- [ ] Create a fallback procedure for when a 'locator' function returns false--causing an issue with 'clear_input' -- currently has a bandaid but needs to be updated properly
- [ ] If 'number_results' is 1, check for previously_downloaded if 'download_only' options is active BEFORE document is opened (unnecessary time glut)
- [ ] Documents with the same reception numbers should be downloaded successively with "-#" based on the result number
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
- [ ] Rebuild 'download_list' function from eagle execute--torn apart from consolidating review function
- [ ] Add 'start_time' as an optional argument for document found depending on download state
- [ ] Create create option in 'handle_search_results' to account for 'else'
- [ ] Create a validation script for eagle
- [ ] Scrub comments from scripts
- [ ] Refactor 'record' script into its own directory
- [ ] Remove an additional space when dropping "see record" in order to cut the new line character out
- [ ] Create a double-check option for eagle--possibly under the "review" as a switch in order to check for any related documents missing
- [ ] Compare the 'switch_into_frame' and dependent 'access_pdf_viewer' functions from the 'download' (and 'record'?) script to try and extrapolate into the generalized 'frame_handling' script
- [ ] Document does not need to be recorded in the 'handle_single_document' function if 'review' is true--create some sort of replacement to only acknowledge that the document has been 'found' ('document_found')
- [ ] Create function logic for the 'record' function of the 'record' script to only grab the 'reception_number' if 'review' or 'download_only' are true
- [ ] Consider eliminating the 'review_entry' function path of the 'record' script--doesn't seem to be in use (could determine if log files are developed)
- [ ] Refactor all of the pdf viewer handling in the 'download' script
- [ ] Add in some semblance of the 'close_program' function used in 'leopard' and 'tiger'

### Iguana To Do

- [ ] Create a new directory to work with the iguana codebase
- [ ] Add all iguana scripts (execute, login, logout, search, open, record, download)
- [ ] Integrate iguana scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution

### Jaguar To Do

- [ ] Needs further manual testing and review
- [ ] Add paths for multiple documents, review, download only, etc.
- [ ] Add a function to drop duplicates (from the document list? from the dataframe?)
- [ ] Add in some semblance of the 'close_program' function used in 'leopard' and 'tiger'
- [ ] Consider combining the 'update_element_attributes' and 'update_document_attributes' functions from the 'transform' script into a single function--downside being specific element attribute updates cannot be extrapolated to a higher level (unless all 'class', 'id', 'tag', etc. attributes are made uniform using an 'attribute' replacement)

### Leopard To Do

- [ ] Update multiple_documents comment to include actual document numbers and / or book & page numbers
- [ ] Remove anything with the "stock download" name before clicking the download button--avoid creating an issue with crash / restart?????
- [ ] Currently the 'download_only' switch for the 'headless' attribute is in the 'execute_program' function--better placement would probably be in the 'environment' or 'initialization' scripts if possible
- [ ] Drop the "if not abstract.download_only and not abstract.review:" line from the 'execute_program' function of the 'execute' script in favor of something more elegant--possibly update on the Abstract or Program class
- [ ] Integrate the 'document.result_number' attribute into the 'handle_multiple_documents' function of the 'execute' script--use eagle as an example template
- [ ] Integrate 'document_downloaded' function from 'file_management' into the 'download' script
- [ ] Integrate 'previously_downloaded' into the 'execute' script instead of calling in the 'download' script--try to set equivalency to the eagle 'execute' script
- [ ] Logic for the 'previously_downloaded' route goes in the 'handle_single_document' function of the 'execute' script
- [ ] Update the 'record' script to set the 'document.reception_number' for the current Document class instance being recorded (somewhere in the 'aggregate_document_information' function of the 'record' script)
- [ ] Create a validation check for 'reception_number', 'book', and 'page' for the 'record' script
- [ ] Extrapolate and generalize the syntax of the 'record_comments' function in leopard 'record' (and all other county engine 'record' scripts)
- [ ] Add element attributes onto Document instances in the 'transform' class

### Mountain Lion

- [ ] Create a new directory to work with the mountain lion codebase
- [ ] Add all mountain lion scripts (execute, login, logout, search, open, record, download)
- [ ] Integrate mountain lion scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution

### Rattlesnake To Do

- [ ] Fix login & search loops for return to home
- [ ] Create a 'volume' & 'page' search
- [ ] Extrapolate access / recording functions in record further to streamline the process further ("id=" will help)
- [ ] Create a convert_document_numbers script
- [ ] Create a "download only" option for execution
- [ ] Update the validation file with the proper use of 'verify' & 'validate' (definitions have been added)
- [ ] Add 'else' logic for 'record' validation
- [ ] Consolidate 'validation' functions in 'validation' script
- [ ] Update 'get downloaded file name' procedure to check for any documents that don't match the correct format in order to avoid renaming the wrong documents
- [ ] Add 'multiple_documents' logic
- [ ] Add 'start_time' as an optional argument for document found depending on download state
- [ ] Create create option in 'handle_search_results' to account for 'else'
- [ ] Refactor 'open_document' selenium functions into selenium utilities directory
- [ ] Refactor 'record' selenium functions into selenium utilities directory
- [ ] Add a method for handling "NO DOCUMENT TYPES"
- [ ] Drop book from Dataframe
- [ ] Add 'search_url' & 'search_title' (and respective 'old') to the document instances with 'transform' script & the document class
- [ ] Update the 'record' script 'record_bad_value' to 'record_invalid_value'
- [ ] Consider extrapolating 'record_bad_value' to the 'invalid' script
- [ ] Create a new 'tiger' directory inside the 'engines' directory
- [ ] Update all scripts to work with the 'Project' and 'Abstract' classes

### Tiger To Do

- [ ] Update multiple_documents comment to include actual document numbers and / or book & page numbers
- [ ] Re-design tiger to work with the code base for leopard
- [ ] Create a logout script to work with tiger -- again based on leopard primarily
- [ ] Refactor environment to work with the new export, document_list, & execute functionality
- [ ] Refactor the 'search' script
- [ ] Refactor the 'open' script
- [ ] Refactor tiger record
- [ ] Refactor tiger download
- [ ] Update record (after refactoring) to work with multiple documents
- [ ] Document.number_results should be spread across open, record, & execute
- [ ] Create a convert_document_numbers script to work like leopard, but with the tiger document lists
- [ ] Create a "download only" option for execution
- [ ] Update scripts with new general functions (i.e. assert_window_title)
- [ ] Update the record function to set the reception number rather than return it
- [ ] Add Book / Page search option to the 'search' script & forward
- [ ] Create a new 'tiger' directory inside the 'engines' directory
- [ ] Update all scripts to work with the 'Project' and 'Abstract' classes
- [ ] Create a 'transform' script to handle updating document numbers and setting document attributes
- [ ] Update the 'execute_web_program' function to work with the original Django / React setup
- [ ] Create a 'logout' script and a 'transform' script
- [ ] Integrate the 'number_results' attribute of the Document class into 'open_document', 'download', 'record', and 'execute'
- [ ] Update the 'search', 'open', 'record', and 'download' scripts to use the passed Document class instance instead of a raw 'document_number' (like they were set up for)
- [ ] Add the 'downloaded_document' or 'no_download'(?) functions into the 'download' script
- [ ] Move the 'javascript_execution' and 'naptime' out of the 'handle_single_document' function---currently looks messy and removing will align the 'handle_single_document' function with other 'execute' scripts
- [ ] Update the 'convert_document_numbers' function in the 'transform' script using the leopard 'convert_document_numbers' function as a model

## Other To Do

### Documentation To Do

- [ ] Create a breakdown of adding a new county ('skeleton structures', 'general_functions', etc.)
- [ ] Create an explanation .md file to define & explain the differences between 'locate', 'get', 'access', 'build', 'handle', etc. functions--'access' & 'get' functions have some overlap, & specifically defining differences would be incredibly beneficial

### Testing Script To Do

- [ ] Needs webdriver, target directory, document class, headless, etc. all aggregated
- [ ] Create a 'testing' script that imports all settings & variables & opens a browser instance so dev setup doesn't have to be completely manual
- [ ] Use the 'testing_dataframe' from the 'objects' directory in the testing script as appropriate
