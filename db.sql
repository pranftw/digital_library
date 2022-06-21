create database pw;
use pw;
create table users(id int primary key auto_increment, first_name varchar(50), last_name varchar(50), email varchar(50), password varchar(100), is_admin tinyint default 0);
create table books(id int primary key auto_increment, title varchar(100), author varchar(100), stocks int, sem int, subject varchar(100), img_url varchar(300));
create table issued(id int primary key auto_increment, book_id int, user_id int, date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, foreign key(book_id) references books(id) on delete cascade on update cascade, foreign key(user_id) references users(id) on delete cascade on update cascade);
create table notify(id int primary key auto_increment,book_id int, user_id int, foreign key(book_id) references books(id) on delete cascade on update cascade, foreign key(user_id) references users(id) on delete cascade on update cascade);
create table requests(id int primary key auto_increment, title varchar(100), author varchar(100));
create table to_be_approved(id int primary key auto_increment, book_id int, user_id int, type_approval varchar(10), foreign key(book_id) references books(id) on delete cascade on update cascade, foreign key(user_id) references users(id) on delete cascade on update cascade);

insert into books(author,title,stocks,img_url,sem,subject) values
('Carl Hamacher Zvonko Vranesic ','Computer Organization And Embedded Systems',0,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHtUefN2X_Fv0Kvk7g5a71vy4KhMoj-KxhGw&usqp=CAU',3,'Computer Organization and Architecture'),
('Thomas Rauber','Parallel Programming for Multicore and Cluster Systems',0,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRir264IIs61urHv5QFZ3H0IZuSbBc1EuSl44E6T0dQYSiJ0cbjUoTYwGxI18NyCxQMHcc&usqp=CAU',3,'Computer Organization and Architecture'),
('David A. Patterson','Computer Organization and Design - The Hardware/Software Interface',0,'https://images-na.ssl-images-amazon.com/images/I/519FtuVhvcL._SX380_BO1,204,203,200_.jpg',3,'Computer Organization and Architecture'),
('William Stallings','Computer Organization & Architecture',0,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSue8XlMd7dAWatrCj5MJ8V8Xact5otFx3qHdKV7izwefcXE8JETugosHUFik9BOyN71pc&usqp=CAU',3,'Computer Organization and Architecture');

insert into books(author,title,stocks,img_url,sem,subject) values
('Herbert Schildt','Java the Complete Reference',0,'https://assetscdn1.paytm.com/images/catalog/product/9/97/9789339212094_81104/1563554899831_1.jpg?imwidth=320&impolicy=hq',3,'Object Oriented Programming with Java'),
('Y. Daniel Liang','Introduction to JAVA Programming',5,'https://images-na.ssl-images-amazon.com/images/I/51lkHc6Hl1L._SX258_BO1,204,203,200_.jpg',3,'Object Oriented Programming with Java'),
('James P Cohoon','Programming in JAVA 5.0',5,'https://images-na.ssl-images-amazon.com/images/I/51PTEBQQMGL._SX375_BO1,204,203,200_.jpg',3,'Object Oriented Programming with Java'),
('E.BalaGuruSwamy','Programming with Java A Primer',5,'https://images-na.ssl-images-amazon.com/images/I/5172ZMKIMfL._SX371_BO1,204,203,200_.jpg',3,'Object Oriented Programming with Java');

insert into books(author,title,stocks,img_url,sem,subject) values
('Donald P Leach','Digital Principles and Applications',5,'https://n2.sdlcdn.com/imgs/i/7/i/DIGITAL-PRINCIPLES-AND-APPLICATIONS-SDL451750130-1-a1c73.jpeg',3,'Logic Design'),
('M Morris Mano','Digital Logic and Computer Design',5,'https://images-na.ssl-images-amazon.com/images/I/41aqH42vY-L._SX258_BO1,204,203,200_.jpg',3,'Logic Design'),
('Donald D Givone','Digital Principles & Design',5,'https://images-na.ssl-images-amazon.com/images/I/51ASw27Xs5L._SX258_BO1,204,203,200_.jpg',3,'Logic Design'),
('R D Sudhaker Samuel','Illustrative Approach to Logic Design',5,'https://images-na.ssl-images-amazon.com/images/I/41qrZHLvnWL._SY344_BO1,204,203,200_.jpg',3,'Logic Design');

insert into books(author,title,stocks,img_url,sem,subject) values
('Horowitz','Fundamentals of Data Structures in C',5,'https://i.pinimg.com/236x/3d/cf/17/3dcf1741e11d7a81c524b2fc68c0a584.jpg',3,'Data Structures'),
('Aaron M.Tenenbaum','Data Structures using C',5,'https://www.pragationline.com/wp-content/uploads/2021/03/DATA-STRUCTURES-USING-C-AND-C-YEDIDYAH-LANGSAM-MOSHE-J.-AUGENSTEIN-ARON-M.-TENENBAUM.jpg',3,'Data Structures'),
('Robert L. Kruse','Data structures and program design in C',5,'https://images-na.ssl-images-amazon.com/images/I/51eyW36STrL._SX359_BO1,204,203,200_.jpg',3,'Data Structures'),
('A.M Padma Reddy','Data Structure using C',5,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRV0Jk_1CqGDKF0h9a9EYNYjYLvq1nwX9AxJA&usqp=CAU',3,'Data Structures');

insert into books(author,title,stocks,img_url,sem,subject) values
('A K Ray and K M Bhurchandi.','Advanced Microprocessor and peripherals',5,'https://booksbeka.com/image/cache/catalog/ANI/download-550x550h.jpg',3,'Microprocessors and Microcontrollers'),
('Kenneth J. Ayala','The 8051 Microcontroller Architecture, Programming & Applications',5,'https://images-na.ssl-images-amazon.com/images/I/51MK9WDSHFL._SX258_BO1,204,203,200_.jpg',3,'Microprocessors and Microcontrollers'),
('Udaya Kumar ','Advanced Microprocessors and IBM - Pc Assembly Language Programming',5,'https://images-na.ssl-images-amazon.com/images/I/71pWc9xz69L.jpg',3,'Microprocessors and Microcontrollers');

insert into books(author,title,stocks,img_url,sem,subject) values
('Seymour Lipchitz. M. Lipson','Discrete Mathematics',5,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvI9OdtXLVl6TiMZhIjSDvTsbsmi5i69qnwoD73JLapieWlCvHDqw9cLOjcq-wOGZ2Bts&usqp=CAU',3,'Statistics and Discrete Mathematics'),
('D. S. Chandrasekharaiah','Graph Theory and Combinatorics',5,'https://rukminim1.flixcart.com/image/312/312/kl9rssw0/book/7/0/u/discrete-mathematical-structures-iiird-sem-4th-edition-b-e-original-imagyfk6ayvgnmtf.jpeg?q=70',3,'Statistics and Discrete Mathematics'),
('B. V. Ramana','Higher Engineering Mathematics',10,'https://images-na.ssl-images-amazon.com/images/I/51Qp2TyOzGL._SX370_BO1,204,203,200_.jpg',3,'Statistics and Discrete Mathematics'),
('Kenneth H. Rosen','Discrete Mathematics and its Applications',3,'https://images-na.ssl-images-amazon.com/images/I/51E75M0Rm5L._SX374_BO1,204,203,200_.jpg',3,'Statistics and Discrete Mathematics');

/* 4th sem */

insert into books(author,title,stocks,img_url,sem,subject) values
('David C. lay','Linear Algebra and its applications',5,'https://images-na.ssl-images-amazon.com/images/I/51xecyCjTKL._SX258_BO1,204,203,200_.jpg',4,'Linear Algebra'),
('Gilbert Strang','Linear Algebra and its applications',5,'https://images-na.ssl-images-amazon.com/images/I/511MUkxPscL.jpg',4,'Linear Algebra'),
('Seymour Lipschutz','Schaum’s outline series-Theory and problems of linear algebra',5,'https://images-na.ssl-images-amazon.com/images/I/51uLJZuctuL.jpg',4,'Linear Algebra'),
('Richard Bronson ','Linear Algebra an Introduction',5,'https://images-eu.ssl-images-amazon.com/images/I/51TTG1OGH6L._SY264_BO1,204,203,200_QL40_ML2_.jpg',4,'Linear Algebra');

insert into books(author,title,stocks,img_url,sem,subject) values
('John E. Hop croft','Introduction to Automata Theory, Languages and Computation',5,'https://rukminim1.flixcart.com/image/416/416/book/8/6/2/introduction-to-automata-theory-languages-and-computation-anna-original-imaekhdauznqzjyk.jpeg?q=70',4,'Theoretical Foundations of Computations'),
('John C Martin','Itroduction to Languages and Automata Theory',5,'https://images-na.ssl-images-amazon.com/images/I/419CV8iqIHL._SX399_BO1,204,203,200_.jpg',4,'Theoretical Foundations of Computations'),
('Peter Linz','An Introduction to formal Languages and Automata',5,'https://images-na.ssl-images-amazon.com/images/I/616UEKjXzPL._SX407_BO1,204,203,200_.jpg',4,'Theoretical Foundations of Computations'),
('Daniel I.A. Cohen','Introduction to Computer Theory',5,'https://media.wiley.com/product_data/coverImage300/23/04711377/0471137723.jpg',4,'Theoretical Foundations of Computations');

insert into books(author,title,stocks,img_url,sem,subject) values
('Ramez Elmasri  ','Fundamental of Database Systems',5,'https://m.media-amazon.com/images/I/515RW73YtIL._SX260_.jpg',4,'Database Management Systems'),
('Ramakrishnan ','Database Management Systems',5,'https://images-na.ssl-images-amazon.com/images/I/41QGbYii3OL.jpg',4,'Database Management Systems'),
('C.J.Date','An Introduction to Database Systems',5,'https://images-na.ssl-images-amazon.com/images/I/5173G0M4QXL._AC_UL600_SR486,600_.jpg',4,'Database Management Systems'),
('Hector GarciaMolina','Database Systems:The Complete Book',5,'https://images-na.ssl-images-amazon.com/images/I/51c7hudZfHL._SX378_BO1,204,203,200_.jpg',4,'Database Management Systems');

insert into books(author,title,stocks,img_url,sem,subject) values
('Anany Levitin','Introduction to the Design and Analysis of Algorithms',5,'https://images-na.ssl-images-amazon.com/images/I/615MSAW2RXL._SX258_BO1,204,203,200_.jpg',4,'Analysis and Design of Algorithms'),
('Thomas H Cormen ','Introduction to Algorithms',5,'https://images-na.ssl-images-amazon.com/images/I/41T0iBxY8FL._SX440_BO1,204,203,200_.jpg',4,'Analysis and Design of Algorithms'),
('Ellis Horowitz','Fundamentals of Computer Algorithms',5,'https://images-na.ssl-images-amazon.com/images/I/51GBoxGlSkL.jpg',4,'Analysis and Design of Algorithms'),
('Padma Reddy','Analysis and design of Algorithms',5,'https://booksbeka.com/image/cache/catalog/00000/ada-550x550h.jpg',4,'Analysis and Design of Algorithms');

insert into books(author,title,stocks,img_url,sem,subject) values
('Abraham Silberschatz','Operating System Concepts',5,'https://media.wiley.com/product_data/coverImage300/55/11180937/1118093755.jpg',4,'Operating Systems'),
('Andrew S.Tanenbaum','Modern Operating System3',5,'https://images-na.ssl-images-amazon.com/images/I/81zfNkDTQLL.jpg',4,'Operating Systems'),
('William Stallings','Operating System: Internals and Design Principles',5,'https://images-na.ssl-images-amazon.com/images/I/51ccTouNn-L.jpg',4,'Operating Systems'),
('J. Archer Harris','Schaums Outline of Operating Systems',5,'https://images-na.ssl-images-amazon.com/images/I/510pE909DTL._SX373_BO1,204,203,200_.jpg',4,'Operating Systems');

insert into books(author,title,stocks,img_url,sem,subject) values
('Merunandan K.B. ','An Introduction to Constitution of India and Professional Ethics',5,'https://images-na.ssl-images-amazon.com/images/I/51gJppe8xrL._SX326_BO1,204,203,200_.jpg',4,'Constitution of India, Professional Ethics and Human Rights'),
('Phaneesh K. R.','Constitution of India &Professional Ethics& Human Rights',5,'https://www.cengage.co.in/Book_images_tn/9789386668479_tn.jpg',4,'Constitution of India, Professional Ethics and Human Rights'),
('Mahendra Pal Singh','V.N. Shukla s Constitution of India',5,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcycPQ9ALjcPVsjz7DQ769eXS8S0q1ZGgvEQ&usqp=CAU',4,'Constitution of India, Professional Ethics and Human Rights'),
('Martin, W. Mike','Ethics in Engineering',5,'https://cdn01.sapnaonline.com/bk_images/932/9780071112932.jpg',4,'Constitution of India, Professional Ethics and Human Rights');

/* 5th sem */

insert into books(author,title,stocks,img_url,sem,subject) values
('Stuart J. Russell','Artificial Intelligence',5,'https://images-na.ssl-images-amazon.com/images/I/51qRNHEQbvL._SX355_BO1,204,203,200_.jpg',5,'Artificial Intelligence'),
('Elaine Rich','Artificial Intelligence',5,'https://images-na.ssl-images-amazon.com/images/I/61CCWFxB90L.jpg',5,'Artificial Intelligence'),
('George F Luger','Artificial Intelligence',10,'https://freecomputerbooks.com/covers/Artificial-Intelligence-Structures-and-Strategies-for-Complex-Problem-Solving.jpg',5,'Artificial Intelligence'),
('WDavid L. Poole ','Artificial Intelligence',3,'https://images-na.ssl-images-amazon.com/images/I/51cWmPO2NBL.jpg',5,'Artificial Intelligence');

insert into books(author,title,stocks,img_url,sem,subject) values
('Behrouz A Forouzan','Data Communications',5,'https://images-na.ssl-images-amazon.com/images/I/71gfvWeTAiL.jpg',5,'Computer Networks'),
('William Stallings','Data and Computer Communication',5,'https://www.pearsonhighered.com/assets/bigcovers/0/1/3/1/0131392050.jpg',5,'Computer Networks'),
('Larry L. Peterson','Computer Networks',10,'https://images-na.ssl-images-amazon.com/images/I/51TxuHs3gwL._SX258_BO1,204,203,200_.jpg',5,'Computer Networks'),
('Peter L Dordal ','An Introduction to Computer Networks',3,'https://cv02.twirpx.net/2657/2657576.jpg?t=20181024015332',5,'Computer Networks');

insert into books(author,title,stocks,img_url,sem,subject) values
('Sumitabha Da','Unix Concepts and  Applications',5,'https://n1.sdlcdn.com/imgs/a/4/7/Unix-Concepts-And-Applications-SDL474560944-1-5fe14.jpg',5,'Unix Shell and System Programming'),
('Terrance Chan','UNIX System  Programming using C++',5,'https://cdn01.sapnaonline.com/bk_images/689/9788120314689.jpg',5,'Unix Shell and System Programming'),
('W. Richard  Stevens','Advanced Programming  in the UNIX  Environment',10,'https://images-na.ssl-images-amazon.com/images/I/51mKuAND2-L._SX258_BO1,204,203,200_.jpg',5,'Unix Shell and System Programming'),
('M.G. Venkatesh  Murthy ','UNIX & Shell  Programming',3,'https://images-na.ssl-images-amazon.com/images/I/413RDWnaW4L._SX380_BO1,204,203,200_.jpg',5,'Unix Shell and System Programming');

insert into books(author,title,stocks,img_url,sem,subject) values
('Ian Somerville','Software Engineering',5,'https://images-na.ssl-images-amazon.com/images/I/81iXn5LPFiL.jpg',5,'Software Engineering'),
('Sari Lawrence  Pfleeger','Software Engineering theory  and Practice',5,'https://images-na.ssl-images-amazon.com/images/I/51w9Jito5kL._SX360_BO1,204,203,200_.jpg',5,'Software Engineering'),
('Waman S Jawadeka','Software Engineering  Principles and Practice',10,'https://d1w7fb2mkkr3kw.cloudfront.net/assets/images/book/lrg/9780/0705/9780070583719.jpg',5,'Software Engineering'),
('Rogers S Pressman ','Software Engineering: A  Practitioners Approach',3,'https://images-na.ssl-images-amazon.com/images/I/81c+Aj3ItcL.jpg',5,'Software Engineering');

insert into books(author,title,stocks,img_url,sem,subject) values
('ArsheepBahga','Internet of Things: A HandsOn Approach',5,'https://images-na.ssl-images-amazon.com/images/I/411WIXXf+eL.jpg',5,'Internet of Things'),
('Michael Margolis','Arduino Cookbook',5,'https://images-na.ssl-images-amazon.com/images/I/91mlVqzFMrL.jpg',5,'Internet of Things'),
('Neil Cameron','Arduino Applied:  Comprehensive Projects for  Everyday Electronics',10,'https://www.oreilly.com/library/view/arduino-applied-comprehensive/9781484239605/images/978-1-4842-3960-5_CoverFigure.jpg',5,'Internet of Things'),
('Brian Evans','Beginning Arduino Programming',3,'https://images-na.ssl-images-amazon.com/images/I/71GkglZA+uL.jpg',5,'Internet of Things');

insert into books(author,title,stocks,img_url,sem,subject) values
('T. H Cormen','Introduction to Algorithms',5,'https://n4.sdlcdn.com/imgs/b/z/6/Introduction-To-Algorithms-Paperback-English-SDL474587042-1-8ecff.jpg',5,'Advanced Data Structures'),
('Marks Allen Wesis','Data Structures and algorithm analysis in C++',5,'https://images-na.ssl-images-amazon.com/images/I/51GBoxGlSkL.jpg',5,'Advanced Data Structures'),
('Ellis Horowitz','Fundamentals of Computer Algorithms',10,'https://images-na.ssl-images-amazon.com/images/I/51F2+CqJ1xL.jpg',5,'Advanced Data Structures'),
('Allen Weiss','Data structures and Algorithm Analysis in C++',3,'https://images-na.ssl-images-amazon.com/images/I/41CVzZKWBxL.jpg',5,'Advanced Data Structures');

/* 6th sem */

insert into books(author,title,stocks,img_url,sem,subject) values
('Behrouz A.Forouzan ','Cryptography and Network Security',5,'https://images-na.ssl-images-amazon.com/images/I/51ghtQ1y-sL._SY445_QL70_ML2_.jpg',6,'Cryptography and Network Security'),
('W. Stallings','Cryptography and Network Security. Principles and Practice',5,'https://images-na.ssl-images-amazon.com/images/I/91reK8vkWVL.jpg',6,'Cryptography and Network Security'),
('Stinson. D','Cryptography: Theory  and Practice',10,'https://images-na.ssl-images-amazon.com/images/I/71SXfuoN3QL.jpg',6,'Cryptography and Network Security'),
('Atul Kahate','Cryptography and Network Security',3,'https://images-na.ssl-images-amazon.com/images/I/61DfbxdVTXL.jpg',6,'Cryptography and Network Security');

insert into books(author,title,stocks,img_url,sem,subject) values
('Seema Acharya','Big Data and Analytics',5,'https://images-na.ssl-images-amazon.com/images/I/41usEaxnGqL._SX258_BO1,204,203,200_.jpg',6,'Big Data Analytics'),
('Andy Konwinski','Learning Spark  Lightning-Fast Big Data  Analysis Principles and Practice',5,'https://images-na.ssl-images-amazon.com/images/I/51qIAkUeuXL._SX379_BO1,204,203,200_.jpg',6,'Big Data Analytics'),
('Radha Shankarmani','Big Data Analytics',10,'https://images-na.ssl-images-amazon.com/images/I/517T33xSuTL._SX258_BO1,204,203,200_.jpg',6,'Big Data Analytics'),
('Cay S. Horstmann','Scala for the Impatient',3,'https://m.media-amazon.com/images/I/51K64Ry6J7L.jpg',6,'Big Data Analytics');

insert into books(author,title,stocks,img_url,sem,subject) values
('M M. Mitchell','Machine Learning',5,'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1387743284l/213030.jpg',6,'Machine Learning'),
('Andreas C Muller ','Introduction to Machine Learning with Python',5,'https://images-eu.ssl-images-amazon.com/images/I/51IXBmHSe1L._SX198_BO1,204,203,200_QL40_ML2_.jpg',6,'Machine Learning'),
('Mathew Kirk','Thoughtful Machine learning',10,'https://images-na.ssl-images-amazon.com/images/I/71XxuVMcKjL.jpg',6,'Machine Learning'),
('Aureliene Geron','Hands-On Machine Learning With Scikit-learn and Tensorflow',3,'https://images-na.ssl-images-amazon.com/images/I/71P4atQpTbL.jpg',6,'Machine Learning');

insert into books(author,title,stocks,img_url,sem,subject) values
('Michael Blaha','Object-Oriented Modeling and Design with UML',5,'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1385396824l/18947244.jpg',6,'Object Oriented Modelling and Design'),
('Nicholas, J. ','Project Management for Business, Engineering and Technology',5,'http://images.tandf.co.uk/common/jackets/crclarge/978008096/9780080967042.jpg',6,'Object Oriented Modelling and Design'),
('Prasanna Chandra','Project Planning, Analysis, Selection, Implementation and Review',10,'https://images-na.ssl-images-amazon.com/images/I/414VS8Uiw6L.jpg',6,'Object Oriented Modelling and Design'),
('Grady Booch et al','ObjectOriented Analysis and Design with Applications',3,'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1347981229l/1751122.jpg',6,'Object Oriented Modelling and Design');

insert into books(author,title,stocks,img_url,sem,subject) values
('Donald Hearn ','Computer Graphics with OpenGL',5,'https://images.bwbcovers.com/013/9780132484572.jpg',6,'Computer Graphics & Visualization'),
('FS Hill ','Computer Graphics using OpenGL',5,'https://pictures.abebooks.com/isbn/9789332555303-us.jpg',6,'Computer Graphics & Visualization'),
('Edward Angel','Interactive Computer Graphics – A Top-down Approach using Opengl',10,'https://images-na.ssl-images-amazon.com/images/I/81oUrvfX6EL.jpg',6,'Computer Graphics & Visualization'),
('Michael Abrash','Graphics Programming Black Book',3,'https://images-na.ssl-images-amazon.com/images/I/41usEaxnGqL._SX258_BO1,204,203,200_.jpg',6,'Computer Graphics & Visualization');

/* 7th sem */

insert into books(author,title,stocks,img_url,sem,subject) values
('Herbert Schild','Java the Complete Reference',5,'https://images-na.ssl-images-amazon.com/images/I/51U232GoNXL._SX258_BO1,204,203,200_.jpg',7,'Java Programming'),
('Y.Daniel Liang','Introduction to JAVA programming',5,'https://images-na.ssl-images-amazon.com/images/I/51hOnFPzUfL.jpg',7,'Java Programming'),
('Patrick Naughton','The Java Hand Book',10,'https://images-na.ssl-images-amazon.com/images/I/51Z8mQwUuUL._SX372_BO1,204,203,200_.jpg',7,'Java Programming'),
('Cay S Horstmann','Core Java 2',3,'https://images-na.ssl-images-amazon.com/images/I/71w0GK2e7eL.jpg',7,'Java Programming');

insert into books(author,title,stocks,img_url,sem,subject) values
('Rajkumar Buyya','CLOUD COMPUTING – Principles and Paradigms',5,'https://media.wiley.com/product_data/coverImage300/90/04708879/0470887990.jpg',7,'Cloud Computing'),
('Anthony T. Velte','Cloud Computing: A practical Approach',5,'https://kbimages1-a.akamaihd.net/d843c9bd-eec5-492e-ae0e-207b9624b511/1200/1200/False/cloud-computing-a-practical-approach-2.jpg',7,'Cloud Computing'),
('Dr. Kumar Saurabh','CLOUD COMPUTING',10,'https://m.media-amazon.com/images/I/51FfBFonLGL._SX260_.jpg',7,'Cloud Computing'),
('Dan C Marinescu','CLOUD COMPUTING – Theory and Practice',3,'https://m.media-amazon.com/images/I/51xfQtlJzHL._SX260_.jpg',7,'Cloud Computing');

insert into books(author,title,stocks,img_url,sem,subject) values
('Kishor S. Trivedi','Probability & Statistics with Reliability, Queuing and Computer Applications',5,'https://media.wiley.com/product_data/coverImage300/17/04713334/0471333417.jpg',7,'Probability , Statistics And Queuing'),
('Raj Jain','The Art of Computer Systems Performance Analysis',5,'https://media.wiley.com/product_data/coverImage300/63/04715033/0471503363.jpg',7,'Probability , Statistics And Queuing'),
('M. Baron','Probability and Statistics for Computer Scientists',10,'https://images-na.ssl-images-amazon.com/images/I/51Kd+nTTYDL.jpg',7,'Probability , Statistics And Queuing'),
('Sheldon Ross','A first course in Probability',3,'https://images-na.ssl-images-amazon.com/images/I/81h5d4d08sL.jpg',7,'Probability , Statistics And Queuing');

insert into books(author,title,stocks,img_url,sem,subject) values
('Jhon R. Vacca','Computer Forensics',5,'https://d1w7fb2mkkr3kw.cloudfront.net/assets/images/book/lrg/9781/5845/9781584503897.jpg',7,'CYBER FORENSICS'),
('Albert J. Marcella Jr.','Cyber Forensics: from Data to Digital Evidence',5,'https://images-na.ssl-images-amazon.com/images/I/71kgfx-4GjL.jpg',7,'CYBER FORENSICS'),
('Pearson Education','Marjie T. Britz: Computer Forensics and Cyber Crime - An Introduction',10,'https://www.pearsonhighered.com/assets/bigcovers/0/1/3/2/0132447495.jpg',7,'CYBER FORENSICS'),
('Computer Forensics','Computer Forensics: Investigating Network Intrusions and Cyber Crime',3,'https://images-na.ssl-images-amazon.com/images/I/51tXnvE%2Bs1L._AC_SY400_.jpg',7,'CYBER FORENSICS');

insert into books(author,title,stocks,img_url,sem,subject) values
('Shameem Akhter ','Multicore Programming , Increased Performance through Software Multi-threading',5,'https://images-na.ssl-images-amazon.com/images/I/81m0vGYmKEL.jpg',7,'Multicore Programming'),
('Michael J. Quinn','Parallel Programming in C with MPI and OpenMP',5,'https://images-na.ssl-images-amazon.com/images/I/714Pv04FNSL.jpg',7,'Multicore Programming'),
('Ananth Grama','Introduction to Parallel Computing',10,'https://images-na.ssl-images-amazon.com/images/I/51dMzTYk0uL._SX307_BO1,204,203,200_.jpg',7,'Multicore Programming'),
('Michael J. Quinn','Parallel Programming in C with MPI and OpenMP',3,'https://images-na.ssl-images-amazon.com/images/I/41xundHlziL._SX331_BO1,204,203,200_.jpg',7,'Multicore Programming');

/* 8th sem */

insert into books(author,title,stocks,img_url,sem,subject) values
('BhuvanUnhelkar','Green IT Strategies and Applications-Using Environmental Intelligence',5,'https://images.routledge.com/common/jackets/crclarge/978042910/9780429105814.jpg',8,'Programming In Python'),
('Woody Leonhard','Green Home computing for dummies',5,'https://images-eu.ssl-images-amazon.com/images/I/51iozCOU4DL._SX342_QL70_ML2_.jpg',8,'Programming In Python'),
('John Lamb','The Greening of IT',10,'https://m.media-amazon.com/images/I/4180sD3WMWL.jpg',8,'Programming In Python'),
('Alin Gales','Green Data Center: Steps for the Journey',3,'https://images-na.ssl-images-amazon.com/images/I/31b+dluLkpL._BO1,204,203,200_.jpg',8,'Programming In Python');

insert into books(author,title,stocks,img_url,sem,subject) values
('Cody Jackson','Learning to Program using Python',5,'https://images-eu.ssl-images-amazon.com/images/I/51c3Tlhi84L._SY445_SX342_QL70_ML2_.jpg',8,'Semantic Web'),
('Michael DAWSON','Python Programming',5,'https://images-na.ssl-images-amazon.com/images/I/51dbifOGAYL.jpg',8,'Semantic Web'),
('Bill Lubanovic','Introducing Python',10,'https://images-na.ssl-images-amazon.com/images/I/91ELJ94KTRL.jpg',8,'Semantic Web'),
('Dr. M. O. FaruqueSarker','Learning Python Network Programming',3,'https://images-eu.ssl-images-amazon.com/images/I/61QP5zR79pL._SX342_QL70_ML2_.jpg',8,'Semantic Web');

insert into books(author,title,stocks,img_url,sem,subject) values
('Liyang Yu','A Developer’s Guide to the Semantic Web',5,'https://images-na.ssl-images-amazon.com/images/I/418OjEOTbFL.jpg',8,'Green Computing'),
('John Hebeler','Semantic Web Programming',5,'https://images-na.ssl-images-amazon.com/images/I/51STP1w5NtL.jpg',8,'Green Computing'),
('Grigoris Antoniou','A Semantic Web Primer',10,'https://mitpress.mit.edu/sites/default/files/styles/large_book_cover/http/mitp-content-server.mit.edu%3A18180/books/covers/cover/%3Fcollid%3Dbooks_covers_0%26isbn%3D9780262018289%26type%3D.jpg?itok=OtqrnFfw',8,'Green Computing'),
('Robert M. Colomb','Ontology and the Semantic Web',3,'https://images-na.ssl-images-amazon.com/images/I/71Ddnqw4gPL.jpg',8,'Green Computing');



