# e-mission-common library

This library contains code that can be used by multiple e-mission components including [e-mission-server](https://github.com/e-mission/e-mission-server), [e-mission-phone](https://github.com/e-mission/e-mission-phone), [em-public-dashboard](https://github.com/e-mission/em-public-dashboard), and [op-admin-dashboard](https://github.com/e-mission/op-admin-dashboard).

This repository uses the [Transcrypt](https://www.transcrypt.org/) library to compile Python code to JavaScript. This allows us to write and maintain code in 1 language and import it for use in all 4 projects.

## Setup

```
pip install transcrypt
```

## To contribute

1. Make your changes to Python code under the `src` directory.
2. Run `. ./bin/compile_to_js.sh` to build the JavaScript. This will produce output JS files in the `emcommon_js` directory.
3. Commit your changes from both the `src` and `emcommon_js` directories.

## Tips for writing code to work in both Python and JavaScript

1. Use the `logger` module for all logs; it is set up to work in both languages.
2. When you need to run a snippet in Python but not in JavaScript, you can use the `skip` pragma to skip one line or multiple lines.
   
    ```python
    Logger.log_info("This line executes in both Python and JavaScript")
    
    Logger.log_info("But this line only executes in in Python") # __: skip
    
    # __pragma__('skip')
    Logger.log_info("This whole block of lines only executes in Python")
    Logger.log_info("JS ignores anything between the skip and noskip pragma comments")
    # __pragma__('noskip')
    
    Logger.log_info("This line is back to executing in both Python and JavaScript")
    ```
4. When you need to run something in JavaScript but not in Python, you can use an **"executable comment"**, which starts with `'''?` and ends with `?'''`.
   
    ```python
    Logger.log_info("This line executes in both Python and JavaScript")
    
    '''?
    Logger.log_info("This only executes in JavaScript")
    Logger.log_info("The Transcrypt compiler will convert this to JavaScript code")
    Logger.log_info("But regular Python will just see it as a comment and ignore it")
    ?'''
    ```
5. If you need to insert raw JavaScript code, you can use the `js` pragma.
   
    ```python
    Logger.log_info("This is Python code that executes in both Python and JavaScript")
    # __pragma__('js', '{}', 'alert("This is raw JavaScript code that executes in JavaScript")')
    ```
    If you need multiple lines of raw JavaScript, you can wrap the `js` pragma in an **"executable comment"**.
   
    ```python
    '''?
    __pragma__('js', '{}', """
      let msg = "This is raw JavaScript code that executes in JavaScript";
      msg += ", and it can be multiple lines";
      alert(msg);
    """)
    ?'''
    ```

For more detail, refer to the Transcrypt docs on the [many kinds of pragmas available.](https://www.transcrypt.org/docs/html/special_facilities.html)
