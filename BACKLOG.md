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

### Error Handling To Do

- [ ] Consider creating an error_handling function for exceptions which takes a screenshot & throws an input together with the above suggestion
- [ ] Add input() to every timeout which doesn't have a natural resolution in order to pause the program at each exception (& create a correction)--maybe something to follow up 'extrapolate_document_value', like 'input(, please review.\nPlease press enter after reviewing error)' + a screenshot

### Runtime To Do

- [ ] Add program_type to the 'started on...' line when starting a program (checks for cases where the wrong program type was chosen & logging in is time extensive)
- [ ] Add a comment indicating how many documents have been completed
- [ ] Update parameter (and then argument) order for all instances of 'document_found' and 'no_document_found'
- [ ] Add a check to the environment file to make sure that the county information is entered correctly before starting the webdriver
- [ ] Create log files on run returning various metrics => create a comment function that takes a comment as an argument and then updates an object to be exported & prints to the screen

### Class To Do

#### Abstract Class To Do

<!-- - [ ] Up-To-Date -->
- [ ] Add 'transform' to abstract initialization dependent on the county
- [ ] Update either the 'Abstract' or 'Project' class to handle whether to export & bundle a project, rather than having the argument inline of the 'execute_program' functions (across directories)

#### County Class To Do

- [ ] If websites & logins are added to the county class the open_site function can be generalized across all scripts
- [ ] The above can also be used for the 'Program' class instead

#### Document Class To Do

- [ ] Update 'document.value' to 'document.search_value' to create a better differentiation between 'document.reception_number'???
- [ ] Turn off 'download' flag if document image is not available?--could be a better solution to checking image available before trying to download
- [ ] Add date / year into the document class in order to add the option to sort by date
- [ ] Consolidate the 'value' attribute and the 'document_value' instance function--too confusing and creating problems
- [ ] Create class functions for 'document_found', 'document_downloaded', 'no_document_found' and 'no_document_downloaded' using the functions from the 'file_management' script

#### Program Class To Do

- [ ] Create a 'Program' class
- [ ] Use the 'Program' class to create a united 'execute' function across multiple directories

#### Project Class To Do

- [ ] Update either the 'Abstract' or 'Project' class to handle whether to export & bundle a project, rather than having the argument inline of the 'execute_program' functions (across directories)

### Project Management To Do

#### Imports To Do

- [ ] Allow user to review the imported excel document & choose the column / columns to run
- [ ] Add download flag to document class & set at import in order to avoid passing the flag around
- [ ] When creating document instances, leave an indication if a book and page instance & a document number instance are on the same line (use the index) in order to create more effective comments---set up for Document class just needs to be implemented
- [ ] If 0 documents are imported, close the program and send a message
- [ ] If download is true and the document is already located in the target document directory, add a medium nap for eagle--in order to do so, add "downloaded" or something similar to the Document class for imports
- [ ] Armadillo, leopard & tiger use convert_document_numbers, maybe make a workspace level script that checks counties against individual 'convert_document_numbers'
- [ ] Update 'display_document_list' to show all available attributes attached to a document
- [ ] Entire header should be created in the settings block, rather than relying on first & last recording dates in the dataframe
- [ ] Compare parallel scripts from leopard & eagle in order to help refactoring

#### Exports To Do

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

#### User Prompts To Do

- [ ] Demo prompts should have a "go back" option

#### File Management To Do

- [ ] Consolidate 'split_book_and_page' and 'split_volume_and_page' functions
- [ ] Change "Document Found" so that it lists either "recorded" or "recorded & downloaded" instead of located
- [ ] Change 'file_management' to 'dataframe_management' & split out functions into multiple utility scripts
- [ ] Best order of operations for file management should be to create the folder first & then put the documents folder inside of it, rather than bundling at the end

#### Download Management To Do

- [ ] Consolidate the prepare, & check functions in download management--had a case where a 500+ page document was clicked & downloaded properly, but 173 in update, 145 in rename, & 140 in prepare raised a value error that it wasn't a file, even though circling back indicated that it was downloaded properly, and with the expected name
- [ ] Along with above, the new function for waiting for a download & then renaming it could probably be worked together in a new logic path
- [ ] The 'document_directory' should be created if 'download' is true but not otherwise
- [ ] Check if 'document_directory' (.exists?) each time a document is downloaded, & create otherwise
- [ ] Search both the 'download_name' (is that the correct attribute) and the 'new_name' when determining if a document has been downloaded or not (previously_downloaded)
- [ ] Create some series of checks (maybe in 'transform' scripts) to check for previously downloaded documents at the outset--just have to be careful about documents with multiple results (but that could probably be handled with the 'number_results' attribute)

### Settings To Do

#### Invalid To Do

- [ ] Integrate appropriate functions from other scripts into the more generalized 'invalid' script, which has replaced the 'bad_search' script
- [ ] Create sub-functions for recording 'invalid' or 'bad' values which can be extrapolated to all working engine scripts
- [ ] Create a better suited method of using the 'no_document_image' function--currently used in 'armadillo', 'rattlesnake' and 'leopard'
- [ ] Determine if any other switches need to be put in place for the 'record_invalid_search' function if the abstract program type is 'review' or 'download_only'--further, this function may do well handling additional program logic overall

### County Programs To Do

#### Armadillo To Do

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

#### Buffalo To Do

- [ ] Add all buffalo scripts (execute, record, download)
- [ ] Integrate buffalo scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution
- [ ] Update buffalo error_handling with use cases -- currently has none
- [ ] Update all scripts to work with the 'Project' and 'Abstract' classes

#### Crocodile To Do

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

#### Dolphin To Do

- [ ] Create a new directory to work with the dolphin codebase
- [ ] Add all dolphin scripts (execute, login, logout, search, open, record, download)
- [ ] Integrate dolphin scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution

#### Eagle To Do

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

#### Iguana To Do

- [ ] Create a new directory to work with the iguana codebase
- [ ] Add all iguana scripts (execute, login, logout, search, open, record, download)
- [ ] Integrate iguana scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution

#### Jaguar To Do

- [ ] Needs further manual testing and review
- [ ] Add paths for multiple documents, review, download only, etc.
- [ ] Add a function to drop duplicates (from the document list? from the dataframe?)

#### Leopard To Do

- [ ] Update multiple_documents comment to include actual document numbers and / or book & page numbers
- [ ] HIGH PRIORITY -- refactor leopard execute
- [ ] move "get_reception_number" around into download document--passing around 'document_number' is redundant & the document can't be downloaded unless it's on the page anyway
- [ ] Remove anything with the "stock download" name before clicking the download button--avoid creating an issue with crash / restart
- [ ] Update scripts with new general functions (i.e. assert_window_title)
- [ ] Update the record function to set the reception number rather than return it
- [ ] Update 'review' loop so that 'review' comes in as True or False, rather than an 'alt' argument
- [ ] Fix the issue with the defunct 'get_reception_number' function in leopard 'execute' script
- [ ] Create a "download_setup" series of functions where if download == yes: create_directory, get current files, change active directory, etc.
- [ ] Circle back to leopard download after completing the above
- [ ] Eliminate the 'alt' options in the 'execute' script in favor of using attributes on Document class instances
- [ ] Update the leopard 'record' script to use the active Abstract and Document class instances
- [ ] Update the leopard 'download' script to use the active Abstract and Document class instances
- [ ] Fix the 'get_reception_number' function in the 'record' script (use the Document class)
- [ ] Currently the 'download_only' switch for the 'headless' attribute is in the 'execute_program' function--better placement would probably be in the 'environment' or 'initialization' scripts if possible
- [ ] Drop the "if not abstract.download_only and not abstract.review:" line from the 'execute_program' function of the 'execute' script in favor of something more elegant--possibly update on the Abstract or Program class
- [ ] Integrate the 'document.result_number' attribute into the 'handle_multiple_documents' function of the 'execute' script--use eagle as an example template
- [ ] Integrate 'document_downloaded' function from 'file_management' into the 'download' script

#### Mountain Lion

- [ ] Create a new directory to work with the mountain lion codebase
- [ ] Add all mountain lion scripts (execute, login, logout, search, open, record, download)
- [ ] Integrate mountain lion scripts to work with the top level environment file
- [ ] Create a convert_document_numbers script
- [ ] Create an "execution", "review", & "download only" option for execution

#### Tiger To Do

- [ ] Update multiple_documents comment to include actual document numbers and / or book & page numbers
- [ ] Re-design tiger to work with the code base for leopard
- [ ] Create a logout script to work with tiger -- again based on leopard primarily
- [ ] Refactor environment to work with the new export, document_list, & execute functionality
- [ ] Refactor the execute script
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

#### Rattlesnake To Do

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

## Testing Script To Do

- [ ] Needs webdriver, target directory, document class, headless, etc. all aggregated
- [ ] Create a 'testing' script that imports all settings & variables & opens a browser instance so dev setup doesn't have to be completely manual

## PDF Merger To Do

- [ ] Update PDF merger to work on a county by county basis
- [ ] Handle cases where a '-1' document is valid

## Documentation To Do

- [ ] Create a breakdown of adding a new county ('skeleton structures', 'general_functions', etc.)
- [ ] Create an explanation .md file to define & explain the differences between 'locate', 'get', 'access', 'build', 'handle', etc. functions--'access' & 'get' functions have some overlap, & specifically defining differences would be incredibly beneficial
