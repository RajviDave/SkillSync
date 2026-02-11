INSERT INTO quiz
(language, difficulty, quistion,
 optionA, optionB, optionC, optionD, correct_option)
VALUES
('react','easy',
'Which function is used to create a React component using hooks?',
'createComponent()',
'useComponent()',
'function or arrow function',
'new Component()',
'C'),

('react','easy',
'Which hook is used to manage state in a functional component?',
'useRef',
'useEffect',
'useState',
'useMemo',
'C'),

('react','easy',
'Which syntax is used to write UI in React?',
'HTML',
'XML',
'JSX',
'JSON',
'C'),

('react','easy',
'Which command is commonly used to create a new React app?',
'npm create react',
'npx create-react-app',
'npm start react',
'npx react-new',
'B'),

('react','easy',
'Which prop is used to pass data from parent to child component?',
'state',
'props',
'context',
'data',
'B'),

-- ---------------- MEDIUM ----------------

('react','medium',
'Which hook is used to perform side effects in a component?',
'useState',
'useMemo',
'useCallback',
'useEffect',
'D'),

('react','medium',
'What is the correct way to update state based on previous state?',
'setCount(count + 1)',
'setCount = count + 1',
'setCount(prev => prev + 1)',
'update(count + 1)',
'C'),

('react','medium',
'Which attribute is used instead of class in JSX?',
'class',
'className',
'cssClass',
'styleClass',
'B'),

('react','medium',
'Which hook is mainly used to access DOM elements directly?',
'useState',
'useRef',
'useEffect',
'useContext',
'B'),

('react','medium',
'Which feature helps to avoid prop drilling in deeply nested components?',
'Refs',
'Fragments',
'Context API',
'Portals',
'C'),

-- ---------------- HARD ----------------

('react','hard',
'Which hook is mainly used to memoize a function?',
'useMemo',
'useCallback',
'useRef',
'useEffect',
'B'),

('react','hard',
'Which lifecycle behavior does useEffect with empty dependency array simulate?',
'componentDidUpdate',
'componentWillUnmount',
'componentDidMount',
'componentWillMount',
'C'),

('react','hard',
'What is the main purpose of React.memo()?',
'To manage state',
'To memoize a component and prevent unnecessary re-renders',
'To handle side effects',
'To create refs',
'B'),

('react','hard',
'Which feature allows rendering children into a DOM node outside the parent hierarchy?',
'Fragments',
'Portals',
'Context',
'Suspense',
'B'),

('react','hard',
'Which technique helps to split bundle and load components lazily?',
'Code splitting with React.lazy',
'Context API',
'Higher Order Components',
'Pure components',
'A'),

('python','easy',
'Which keyword is used to define a function in Python?',
'func','def','function','define','B'),

('python','easy',
'Which data type is used to store a sequence of characters?',
'list','tuple','string','dict','C'),

('python','easy',
'Which function is used to display output in Python?',
'print()','echo()','write()','show()','A'),

('python','easy',
'Which symbol is used for comments in Python?',
'//','#','/* */','--','B'),

('python','easy',
'Which of the following is a valid list declaration?',
'{1,2,3}','(1,2,3)','[1,2,3]','<1,2,3>','C'),

-- ---------------- MEDIUM ----------------

('python','medium',
'What is the output of: len({1,2,2,3}) ?',
'4','3','2','Error','B'),

('python','medium',
'Which keyword is used to handle exceptions?',
'catch','handle','except','error','C'),

('python','medium',
'Which of the following creates a generator?',
'[]','()','{}','yield','D'),

('python','medium',
'Which module is used for regular expressions?',
'regex','re','pyregex','expression','B'),

('python','medium',
'Which method is used to add an element to a set?',
'append()','add()','insert()','push()','B'),

-- ---------------- HARD ----------------

('python','hard',
'What is the main purpose of the GIL (Global Interpreter Lock)?',
'Improve memory usage',
'Allow true parallelism',
'Protect shared memory in CPython',
'Speed up execution',
'C'),

('python','hard',
'Which decorator is used to define a class method?',
'@staticmethod',
'@classmethod',
'@property',
'@abstractmethod',
'B'),

('python','hard',
'Which statement is true about deep copy and shallow copy?',
'Both create independent objects',
'Shallow copy copies nested objects recursively',
'Deep copy copies all nested objects',
'Deep copy shares references',
'C'),

('python','hard',
'Which of the following is used to make a function remember its state?',
'closure',
'lambda',
'decorator',
'context manager',
'A'),

('python','hard',
'Which protocol allows an object to be used in a for-loop?',
'Callable protocol',
'Iterator protocol',
'Descriptor protocol',
'Context manager protocol',
'B'),

('java','easy',
'Which keyword is used to define a class in Java?',
'class','struct','object','define','A'),

('java','easy',
'Which method is the entry point of a Java program?',
'start()','run()','main()','init()','C'),

('java','easy',
'Which keyword is used to inherit a class?',
'implements','extends','inherits','super','B'),

('java','easy',
'Which of the following is not a primitive data type in Java?',
'int','float','String','char','C'),

('java','easy',
'Which package is automatically imported in every Java program?',
'java.io','java.lang','java.util','java.net','B'),

-- ---------------- MEDIUM ----------------

('java','medium',
'Which concept allows multiple methods with the same name but different parameters?',
'Overriding','Overloading','Inheritance','Encapsulation','B'),

('java','medium',
'Which keyword is used to prevent inheritance?',
'static','final','private','const','B'),

('java','medium',
'Which interface provides dynamic array functionality?',
'List','Set','Map','Queue','A'),

('java','medium',
'Which collection does not allow duplicate elements?',
'ArrayList','LinkedList','HashSet','Vector','C'),

('java','medium',
'Which keyword is used to throw an exception manually?',
'throws','throw','exception','raise','B'),

-- ---------------- HARD ----------------

('java','hard',
'Which of the following is true about Java garbage collection?',
'It frees objects referenced by variables',
'It automatically deletes all unused files',
'It removes objects that are no longer reachable',
'It must be called explicitly by the programmer',
'C'),

('java','hard',
'Which keyword is used to make a variable visible across threads reliably?',
'static','final','volatile','synchronized','C'),

('java','hard',
'Which interface is used to define a task for a thread that returns a result?',
'Runnable','Thread','Callable','Executor','C'),

('java','hard',
'Which statement is true about equals() and hashCode()?',
'They must always return same value',
'If equals is true, hashCode must be same',
'If hashCode is same, equals must be true',
'They are unrelated',
'B'),

('java','hard',
'Which Java feature enables lazy loading and method interception in frameworks?',
'Reflection',
'Serialization',
'Dynamic proxies',
'Annotations',
'C'),

('nodejs','easy',
'Which JavaScript engine is used by Node.js?',
'SpiderMonkey',
'Chakra',
'V8',
'Rhino',
'C'),

('nodejs','easy',
'Which module is used to create a web server in Node.js?',
'http',
'net',
'server',
'web',
'A'),

('nodejs','easy',
'Which command initializes a new Node.js project?',
'npm start',
'npm init',
'node init',
'init npm',
'B'),

('nodejs','easy',
'Which object is used to export functions from a module?',
'exports',
'module.exports',
'export',
'require',
'B'),

('nodejs','easy',
'Which function is used to include a module?',
'import()',
'load()',
'require()',
'include()',
'C'),

-- ---------------- MEDIUM ----------------

('nodejs','medium',
'Which package manager is most commonly used with Node.js?',
'pip',
'composer',
'npm',
'maven',
'C'),

('nodejs','medium',
'Which of the following is used to handle asynchronous operations in Node.js?',
'Thread pools only',
'Callbacks / Promises / async-await',
'Blocking I/O',
'Synchronous functions only',
'B'),

('nodejs','medium',
'Which object represents the current process in Node.js?',
'process',
'current',
'runtime',
'thread',
'A'),

('nodejs','medium',
'Which method is used to read a file asynchronously using fs module?',
'fs.read()',
'fs.readFile()',
'fs.open()',
'fs.load()',
'B'),

('nodejs','medium',
'Which framework is commonly used to build REST APIs in Node.js?',
'Flask',
'Django',
'Express',
'Spring',
'C'),

-- ---------------- HARD ----------------

('nodejs','hard',
'Which concept allows Node.js to handle many connections using a single thread?',
'Multithreading',
'Worker threads',
'Event-driven non-blocking I/O',
'Process forking',
'C'),

('nodejs','hard',
'Which object is used to handle streams of data in Node.js?',
'Buffer',
'Stream',
'Pipe',
'Chunk',
'B'),

('nodejs','hard',
'Which method is used to handle unhandled promise rejections globally?',
'process.on("rejection")',
'process.on("unhandledRejection")',
'process.catch()',
'Promise.onReject()',
'B'),

('nodejs','hard',
'Which technique is commonly used to scale Node.js applications across CPU cores?',
'Clustering',
'Spawning',
'Threading',
'Load balancing only',
'A'),

('nodejs','hard',
'Which API is used to create worker threads in Node.js?',
'cluster',
'child_process',
'worker_threads',
'os',
'C'),

('kotlin','easy',
'Which keyword is used to declare a variable whose value cannot change?',
'var','val','let','const','B'),

('kotlin','easy',
'Which function is used to print output in Kotlin?',
'print()','println()','echo()','write()','B'),

('kotlin','easy',
'Which keyword is used to define a function in Kotlin?',
'fun','function','def','fn','A'),

('kotlin','easy',
'Which type is used to represent true or false values?',
'Boolean','Bool','bit','flag','A'),

('kotlin','easy',
'Which keyword is used to create a class in Kotlin?',
'class','object','struct','type','A'),

-- ---------------- MEDIUM ----------------

('kotlin','medium',
'Which feature helps avoid NullPointerException in Kotlin?',
'Exception handling',
'Garbage collection',
'Null safety',
'Type casting',
'C'),

('kotlin','medium',
'Which operator is used for safe calls?',
'.','?.','!!','::','B'),

('kotlin','medium',
'Which keyword is used to create a singleton object?',
'class','data','object','sealed','C'),

('kotlin','medium',
'Which collection type does not allow duplicate elements?',
'List','Array','Set','Map','C'),

('kotlin','medium',
'Which function is used to iterate over a collection?',
'loop()','forEach()','mapEach()','iterate()','B'),

-- ---------------- HARD ----------------

('kotlin','hard',
'Which keyword is used to represent a class that can have restricted subclasses?',
'sealed','final','open','abstract','A'),

('kotlin','hard',
'Which feature allows functions to be added to existing classes without modifying them?',
'Inheritance',
'Extension functions',
'Overloading',
'Delegation',
'B'),

('kotlin','hard',
'Which coroutine builder launches a new coroutine without blocking the current thread?',
'async',
'launch',
'runBlocking',
'withContext',
'B'),

('kotlin','hard',
'Which modifier allows a class to be inherited by other classes?',
'open',
'public',
'override',
'extend',
'A'),

('kotlin','hard',
'Which Kotlin feature is mainly used to represent restricted class hierarchies?',
'enum classes',
'data classes',
'sealed classes',
'inline classes',
'C'),

('swift','easy',
'Which keyword is used to declare a constant in Swift?',
'let','var','const','final','A'),

('swift','easy',
'Which keyword is used to declare a variable in Swift?',
'let','var','value','mutable','B'),

('swift','easy',
'Which type is used to store true or false values?',
'Bool','Boolean','bit','flag','A'),

('swift','easy',
'Which function is used to print output in Swift?',
'print()','println()','echo()','write()','A'),

('swift','easy',
'Which symbol is used for single line comments in Swift?',
'//','#','--','/* */','A'),

-- ---------------- MEDIUM ----------------

('swift','medium',
'Which feature is used to safely handle the absence of a value?',
'Generics',
'Protocols',
'Optionals',
'Closures',
'C'),

('swift','medium',
'Which keyword is used to unwrap an optional safely?',
'try','guard','unwrap','safe',
'B'),

('swift','medium',
'Which statement is commonly used for pattern matching in Swift?',
'if',
'for',
'switch',
'when',
'C'),

('swift','medium',
'Which keyword is used to define a function in Swift?',
'func','function','def','fn','A'),

('swift','medium',
'Which collection stores unique values?',
'Array',
'List',
'Set',
'Dictionary',
'C'),

-- ---------------- HARD ----------------

('swift','hard',
'Which concept allows passing functions as parameters in Swift?',
'Inheritance',
'Protocols',
'Closures',
'Extensions',
'C'),

('swift','hard',
'Which keyword is used to define a protocol?',
'interface',
'protocol',
'contract',
'trait',
'B'),

('swift','hard',
'Which feature allows adding functionality to existing types?',
'Inheritance',
'Extensions',
'Overloading',
'Delegation',
'B'),

('swift','hard',
'Which mechanism is used for automatic memory management in Swift?',
'Garbage Collection',
'ARC',
'Manual Free',
'Reference Counting Library',
'B'),

('swift','hard',
'Which keyword is used to indicate a throwing function?',
'throws',
'throwable',
'error',
'catch',
'A'),

('dart','easy',
'Which keyword is used to declare a variable in Dart?',
'var','let','def','auto','A'),

('dart','easy',
'Which function is used to print output in Dart?',
'print()','println()','echo()','write()','A'),

('dart','easy',
'Which keyword is used to declare a constant value?',
'final','const','static','fixed','B'),

('dart','easy',
'Which data type represents true or false values?',
'Boolean','Bool','bool','bit','C'),

('dart','easy',
'Which keyword is used to define a function in Dart?',
'fun','function','def','No keyword is required','D'),

-- ---------------- MEDIUM ----------------

('dart','medium',
'Which keyword is used to create an asynchronous function?',
'await','async','future','defer','B'),

('dart','medium',
'Which class represents a value that will be available in the future?',
'Promise','Future','Stream','Task','B'),

('dart','medium',
'Which collection type stores unique elements?',
'List','Set','Map','Queue','B'),

('dart','medium',
'Which operator is used for null-aware access?',
'.','?.','!!','::','B'),

('dart','medium',
'Which keyword is used to inherit a class?',
'extends','implements','inherits','super','A'),

-- ---------------- HARD ----------------

('dart','hard',
'Which feature allows providing multiple constructors with different names?',
'Factory constructors',
'Named constructors',
'Private constructors',
'Static constructors',
'B'),

('dart','hard',
'Which keyword is used to define a constant constructor?',
'const','final','static','fixed','A'),

('dart','hard',
'Which type of function does not have a name in Dart?',
'Closure','Generator','Anonymous function','Factory function','C'),

('dart','hard',
'Which concept allows a class to implement multiple interfaces?',
'Inheritance',
'Multiple inheritance',
'Interface implementation',
'Delegation',
'C'),

('dart','hard',
'Which keyword is used to mark a method that must be implemented by subclasses?',
'override',
'abstract',
'virtual',
'required',
'B');

