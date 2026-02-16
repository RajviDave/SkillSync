INSERT INTO quiz
(language, difficulty, question,
 optionA, optionB, optionC, optionD, correct_option)
VALUES
('r','easy',
'Which symbol is used for assignment in R?',
'=','<-','->',':=','B'),

('r','easy',
'Which function is used to print output in R?',
'print()','cat()','show()','display()','A'),

('r','easy',
'Which function is used to get help on a topic in R?',
'help()','doc()','manual()','info()','A'),

('r','easy',
'Which data structure stores elements of the same type?',
'list','vector','data frame','matrix','B'),

('r','easy',
'Which function is used to read a CSV file in R?',
'read.csv()','load.csv()','import.csv()','open.csv()','A'),

-- ---------------- MEDIUM ----------------

('r','medium',
'Which function is used to apply a function over rows or columns of a matrix?',
'apply()','lapply()','sapply()','tapply()','A'),

('r','medium',
'Which package is commonly used for data manipulation using verbs like filter and select?',
'ggplot2','dplyr','tidyr','shiny','B'),

('r','medium',
'Which function is used to combine data frames by columns?',
'merge()','cbind()','rbind()','join()','B'),

('r','medium',
'Which data structure can store elements of different types?',
'vector','matrix','list','array','C'),

('r','medium',
'Which operator is used for logical AND in R?',
'&','&&','and','Both & and &&','D'),

-- ---------------- HARD ----------------

('r','hard',
'Which function is used to fit a linear regression model in R?',
'lm()','glm()','regress()','fit()','A'),

('r','hard',
'Which function is used to set a random seed for reproducibility?',
'set.seed()','random.seed()','seed()','fix.seed()','A'),

('r','hard',
'Which object type is returned by lm()?',
'data frame','list','model object','matrix','C'),

('r','hard',
'Which function is used to reshape data from wide to long format in tidyr?',
'gather()','spread()','separate()','unite()','A'),

('r','hard',
'Which package is commonly used to create interactive web applications in R?',
'ggplot2','caret','shiny','plotly','C'),

('sql','easy',
'Which SQL statement is used to retrieve data from a table?',
'GET','FETCH','SELECT','READ','C'),

('sql','easy',
'Which clause is used to filter rows in a query?',
'FILTER','WHERE','GROUP','HAVING','B'),

('sql','easy',
'Which keyword is used to remove duplicate rows in a SELECT query?',
'UNIQUE','DISTINCT','ONLY','DIFFERENT','B'),

('sql','easy',
'Which statement is used to insert new data into a table?',
'ADD','INSERT INTO','PUT','UPDATE','B'),

('sql','easy',
'Which operator is used to match a pattern in SQL?',
'MATCH','LIKE','FIND','REGEX','B'),

-- ---------------- MEDIUM ----------------

('sql','medium',
'Which clause is used to group rows that have the same values?',
'ORDER BY','GROUP BY','CLUSTER BY','PARTITION BY','B'),

('sql','medium',
'Which function returns the number of rows?',
'COUNT()','SUM()','TOTAL()','ROWS()','A'),

('sql','medium',
'Which join returns only matching rows from both tables?',
'LEFT JOIN','RIGHT JOIN','FULL JOIN','INNER JOIN','D'),

('sql','medium',
'Which clause is used to filter aggregated results?',
'WHERE','HAVING','GROUP BY','ORDER BY','B'),

('sql','medium',
'Which keyword is used to sort the result set?',
'SORT BY','ORDER','ORDER BY','GROUP','C'),

-- ---------------- HARD ----------------

('sql','hard',
'Which normal form removes partial dependency?',
'1NF','2NF','3NF','BCNF','B'),

('sql','hard',
'Which index type is most commonly used in relational databases?',
'HASH index','BTREE index','BITMAP index','RTREE index','B'),

('sql','hard',
'Which isolation level prevents dirty reads but allows non-repeatable reads?',
'READ UNCOMMITTED','READ COMMITTED','REPEATABLE READ','SERIALIZABLE','B'),

('sql','hard',
'Which window function assigns a unique sequential integer to rows?',
'RANK()','DENSE_RANK()','ROW_NUMBER()','COUNT()','C'),

('sql','hard',
'Which command is used to permanently remove a table and its data?',
'DELETE','REMOVE','DROP','TRUNCATE','C'),

('scala','easy',
'Which keyword is used to define an immutable variable in Scala?',
'var','let','val','const','C'),

('scala','easy',
'Which keyword is used to define a mutable variable in Scala?',
'var','val','mutable','set','A'),

('scala','easy',
'Which keyword is used to define a function in Scala?',
'function','def','fun','fn','B'),

('scala','easy',
'Which object is the entry point of a Scala application?',
'Main','Program','App','object with main method','D'),

('scala','easy',
'Which data type represents a sequence of elements in Scala?',
'Array','List','Set','All of the above','D'),

-- ---------------- MEDIUM ----------------

('scala','medium',
'Which feature allows defining behavior that can be mixed into classes?',
'Inheritance',
'Traits',
'Interfaces',
'Abstract classes',
'B'),

('scala','medium',
'Which keyword is used to perform pattern matching?',
'match',
'switch',
'case',
'when',
'A'),

('scala','medium',
'Which collection preserves insertion order and allows duplicates?',
'Set',
'Map',
'List',
'Option',
'C'),

('scala','medium',
'Which type represents an optional value in Scala?',
'Nullable',
'Maybe',
'Option',
'Either',
'C'),

('scala','medium',
'Which function is commonly used to transform each element of a collection?',
'filter',
'reduce',
'foreach',
'map',
'D'),

-- ---------------- HARD ----------------

('scala','hard',
'Which concept allows functions to be treated as values?',
'Encapsulation',
'First-class functions',
'Inheritance',
'Overloading',
'B'),

('scala','hard',
'Which type is used to represent computations that may fail?',
'Option',
'Try',
'Future',
'Either',
'B'),

('scala','hard',
'Which keyword is used to define a case class?',
'case',
'class',
'data',
'record',
'A'),

('scala','hard',
'Which feature enables lazy evaluation of values?',
'lazy val',
'defer',
'lateinit',
'optional',
'A'),

('scala','hard',
'Which abstraction is mainly used for asynchronous computations in Scala?',
'Thread',
'Promise',
'Future',
'Task',
'C'),

('go','easy',
'Which keyword is used to declare a variable in Go?',
'var','let','def','auto','A'),

('go','easy',
'Which package is required to print output in Go?',
'io','fmt','print','output','B'),

('go','easy',
'Which function is the entry point of a Go program?',
'start()','run()','main()','init()','C'),

('go','easy',
'Which keyword is used to define a constant?',
'const','final','static','let','A'),

('go','easy',
'Which symbol is used for single line comments in Go?',
'//','#','--','/* */','A'),

-- ---------------- MEDIUM ----------------

('go','medium',
'Which keyword is used to start a concurrent function call?',
'async','go','thread','spawn','B'),

('go','medium',
'Which data structure is used to store key–value pairs in Go?',
'list','array','map','struct','C'),

('go','medium',
'Which keyword is used to define a structure type?',
'struct','class','record','object','A'),

('go','medium',
'Which statement is used to receive a value from a channel?',
'receive','<-','=>','get','B'),

('go','medium',
'Which keyword is used to create a package-level initialization function?',
'start','setup','init','boot','C'),

-- ---------------- HARD ----------------

('go','hard',
'Which feature is used in Go to achieve polymorphism without inheritance?',
'Struct embedding',
'Interfaces',
'Generics',
'Reflection',
'B'),

('go','hard',
'Which statement is true about goroutines?',
'They are OS threads',
'They are lightweight threads managed by the Go runtime',
'They block the main thread by default',
'They require explicit synchronization always',
'B'),

('go','hard',
'Which channel type only allows sending values?',
'chan int',
'<-chan int',
'chan<- int',
'sendchan int',
'C'),

('go','hard',
'Which package is commonly used to synchronize goroutines?',
'atomic',
'sync',
'context',
'runtime',
'B'),

('go','hard',
'What happens when a receive operation is performed on a closed channel?',
'Program panics',
'Returns zero value immediately',
'Blocks forever',
'Skips the receive',
'B'),

('bash','easy',
'Which symbol is used to start a bash script file?',
'//','#','#!','/*','C'),

('bash','easy',
'Which command is used to print text to the terminal?',
'print','echo','show','write','B'),

('bash','easy',
'Which command is used to list files in a directory?',
'dir','list','ls','show','C'),

('bash','easy',
'Which command shows the current working directory?',
'pwd','cwd','path','where','A'),

('bash','easy',
'Which symbol is used to access the value of a variable?',
'@','$','%','&','B'),

-- ---------------- MEDIUM ----------------

('bash','medium',
'Which command is used to change file permissions?',
'chown','chmod','setperm','perm','B'),

('bash','medium',
'Which operator is used to redirect output to a file (overwrite)?',
'>','>>','<','|','A'),

('bash','medium',
'Which command is used to search for a pattern in a file?',
'find','locate','grep','search','C'),

('bash','medium',
'Which statement is used for conditional execution in bash?',
'switch','if','when','select','B'),

('bash','medium',
'Which command is used to read user input from terminal?',
'input','read','scan','gets','B'),

-- ---------------- HARD ----------------

('bash','hard',
'Which special variable stores the exit status of the last command?',
'$0','$1','$$','$?','D'),

('bash','hard',
'Which command replaces the current shell with another program?',
'run','exec','spawn','call','B'),

('bash','hard',
'Which operator is used to pipe the output of one command to another?',
'>','<','|','&','C'),

('bash','hard',
'Which option with set command causes the script to exit on error?',
'set -v','set -x','set -e','set -u','C'),

('bash','hard',
'Which test operator checks if a file exists and is a regular file?',
'-d','-e','-f','-r','C'),

('c#','easy',
'Which keyword is used to define a class in C#?',
'class','struct','object','define','A'),

('c#','easy',
'Which method is the entry point of a C# console application?',
'start()','run()','Main()','init()','C'),

('c#','easy',
'Which keyword is used to create an object in C#?',
'new','create','make','alloc','A'),

('c#','easy',
'Which of the following is a value type in C#?',
'string','class','int','object','C'),

('c#','easy',
'Which keyword is used to inherit a class in C#?',
'extends','inherits',':','implements','C'),

-- ---------------- MEDIUM ----------------

('c#','medium',
'Which feature allows multiple methods with the same name but different parameters?',
'Overriding','Overloading','Inheritance','Abstraction','B'),

('c#','medium',
'Which keyword is used to define a method that can be overridden?',
'sealed','static','virtual','override','C'),

('c#','medium',
'Which collection stores key-value pairs?',
'List','Array','Dictionary','Queue','C'),

('c#','medium',
'Which keyword is used to handle exceptions?',
'catch','handle','except','try','D'),

('c#','medium',
'Which keyword makes a member accessible only within the same class?',
'public','internal','private','protected','C'),

-- ---------------- HARD ----------------

('c#','hard',
'Which feature allows querying collections using SQL-like syntax?',
'Entity Framework','LINQ','ADO.NET','Reflection','B'),

('c#','hard',
'Which keyword is used to prevent a class from being inherited?',
'static','sealed','readonly','final','B'),

('c#','hard',
'Which type is used to represent asynchronous operations?',
'Thread','Task','Future','Job','B'),

('c#','hard',
'Which concept allows defining a method without implementation in a base class?',
'Virtual method','Static method','Abstract method','Extension method','C'),

('c#','hard',
'Which keyword ensures that a field is safely accessed across multiple threads?',
'readonly','volatile','lock','sync','B'),

('solidity','easy',
'Which keyword is used to define a smart contract in Solidity?',
'contract','class','module','package','A'),

('solidity','easy',
'Which file extension is used for Solidity source files?',
'.sol','.eth','.sc','.block','A'),

('solidity','easy',
'Which keyword is used to declare a variable that cannot be modified?',
'static','const','immutable','final','C'),

('solidity','easy',
'Which type represents an Ethereum account address?',
'string','address','account','uint','B'),

('solidity','easy',
'Which function is executed when Ether is sent directly to a contract?',
'constructor()','fallback()','receive()','payable()','C'),

-- ---------------- MEDIUM ----------------

('solidity','medium',
'Which keyword allows a function to receive Ether?',
'transfer','receive','value','payable','D'),

('solidity','medium',
'Which global object provides information about the current block?',
'tx','block','msg','chain','B'),

('solidity','medium',
'Which statement is used to revert a transaction and refund remaining gas?',
'stop()','throw','revert()','rollback()','C'),

('solidity','medium',
'Which visibility specifier makes a function callable only inside the same contract?',
'public','external','internal','private','D'),

('solidity','medium',
'Which data location keyword stores variables permanently on the blockchain?',
'memory','stack','storage','calldata','C'),

-- ---------------- HARD ----------------

('solidity','hard',
'Which function is commonly used to prevent re-entrancy attacks?',
'onlyOwner()',
'nonReentrant()',
'secure()',
'lockCall()',
'B'),

('solidity','hard',
'Which of the following is the main cause of re-entrancy vulnerabilities?',
'Integer overflow',
'Unchecked return values',
'External calls before state updates',
'Gas limit exhaustion',
'C'),

('solidity','hard',
'Which feature allows upgrading contract logic while keeping the same storage?',
'Inheritance',
'Library linking',
'Proxy pattern',
'Delegate pattern',
'C'),

('solidity','hard',
'Which opcode is mainly used by delegatecall in proxy contracts?',
'CALL',
'STATICCALL',
'DELEGATECALL',
'CREATE',
'C'),

('solidity','hard',
'Which mechanism is recommended to safely handle arithmetic operations in older Solidity versions?',
'try/catch',
'SafeMath library',
'assert statements',
'manual checks only',
'B');

