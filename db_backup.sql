--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cabinets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cabinets (
    id integer NOT NULL,
    name character varying(63),
    itemcount integer NOT NULL,
    item integer NOT NULL
);


ALTER TABLE public.cabinets OWNER TO postgres;

--
-- Name: cabinets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cabinets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cabinets_id_seq OWNER TO postgres;

--
-- Name: cabinets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cabinets_id_seq OWNED BY public.cabinets.id;


--
-- Name: cities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cities (
    id integer NOT NULL,
    name character varying(255)
);


ALTER TABLE public.cities OWNER TO postgres;

--
-- Name: cities_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cities_id_seq OWNER TO postgres;

--
-- Name: cities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cities_id_seq OWNED BY public.cities.id;


--
-- Name: exam_instance_student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exam_instance_student (
    student_id integer NOT NULL,
    exam_instance_id integer NOT NULL,
    cabinet_id integer,
    mark integer
);


ALTER TABLE public.exam_instance_student OWNER TO postgres;

--
-- Name: exam_instances; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exam_instances (
    id integer NOT NULL,
    max_students integer,
    exam_id integer,
    profile boolean,
    date date
);


ALTER TABLE public.exam_instances OWNER TO postgres;

--
-- Name: exam_instances_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exam_instances_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exam_instances_id_seq OWNER TO postgres;

--
-- Name: exam_instances_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exam_instances_id_seq OWNED BY public.exam_instances.id;


--
-- Name: exams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exams (
    id integer NOT NULL,
    name character varying(255)
);


ALTER TABLE public.exams OWNER TO postgres;

--
-- Name: exams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exams_id_seq OWNER TO postgres;

--
-- Name: exams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exams_id_seq OWNED BY public.exams.id;


--
-- Name: grade_exam_set; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grade_exam_set (
    gradetype_id integer,
    exam_id integer,
    profile boolean
);


ALTER TABLE public.grade_exam_set OWNER TO postgres;

--
-- Name: gradeset; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gradeset (
    student_id integer,
    grade_id integer
);


ALTER TABLE public.gradeset OWNER TO postgres;

--
-- Name: gradetypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gradetypes (
    id integer NOT NULL,
    name character varying(63)
);


ALTER TABLE public.gradetypes OWNER TO postgres;

--
-- Name: gradetypes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gradetypes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gradetypes_id_seq OWNER TO postgres;

--
-- Name: gradetypes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gradetypes_id_seq OWNED BY public.gradetypes.id;


--
-- Name: languages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.languages (
    id integer NOT NULL,
    name character varying(255),
    localname character(255)
);


ALTER TABLE public.languages OWNER TO postgres;

--
-- Name: languages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.languages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.languages_id_seq OWNER TO postgres;

--
-- Name: languages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.languages_id_seq OWNED BY public.languages.id;


--
-- Name: languageset; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.languageset (
    student_id integer,
    primary_id integer,
    foreign_id integer
);


ALTER TABLE public.languageset OWNER TO postgres;

--
-- Name: schools; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.schools (
    id integer NOT NULL,
    city_id integer,
    name character varying(511)
);


ALTER TABLE public.schools OWNER TO postgres;

--
-- Name: schools_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.schools_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schools_id_seq OWNER TO postgres;

--
-- Name: schools_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.schools_id_seq OWNED BY public.schools.id;


--
-- Name: student_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student_status (
    id integer NOT NULL,
    name character varying(255)
);


ALTER TABLE public.student_status OWNER TO postgres;

--
-- Name: student_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_status_id_seq OWNER TO postgres;

--
-- Name: student_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_status_id_seq OWNED BY public.student_status.id;


--
-- Name: students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students (
    id integer NOT NULL,
    name character varying(255),
    school_id integer,
    phone character varying(32),
    adress character varying(255),
    status_id integer
);


ALTER TABLE public.students OWNER TO postgres;

--
-- Name: students_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.students_id_seq OWNER TO postgres;

--
-- Name: students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.students_id_seq OWNED BY public.students.id;


--
-- Name: teachers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teachers (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.teachers OWNER TO postgres;

--
-- Name: teachers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teachers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teachers_id_seq OWNER TO postgres;

--
-- Name: teachers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teachers_id_seq OWNED BY public.teachers.id;


--
-- Name: cabinets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cabinets ALTER COLUMN id SET DEFAULT nextval('public.cabinets_id_seq'::regclass);


--
-- Name: cities id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cities ALTER COLUMN id SET DEFAULT nextval('public.cities_id_seq'::regclass);


--
-- Name: exam_instances id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_instances ALTER COLUMN id SET DEFAULT nextval('public.exam_instances_id_seq'::regclass);


--
-- Name: exams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exams ALTER COLUMN id SET DEFAULT nextval('public.exams_id_seq'::regclass);


--
-- Name: gradetypes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gradetypes ALTER COLUMN id SET DEFAULT nextval('public.gradetypes_id_seq'::regclass);


--
-- Name: languages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languages ALTER COLUMN id SET DEFAULT nextval('public.languages_id_seq'::regclass);


--
-- Name: schools id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools ALTER COLUMN id SET DEFAULT nextval('public.schools_id_seq'::regclass);


--
-- Name: student_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_status ALTER COLUMN id SET DEFAULT nextval('public.student_status_id_seq'::regclass);


--
-- Name: students id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students ALTER COLUMN id SET DEFAULT nextval('public.students_id_seq'::regclass);


--
-- Name: teachers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachers ALTER COLUMN id SET DEFAULT nextval('public.teachers_id_seq'::regclass);


--
-- Data for Name: cabinets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cabinets (id, name, itemcount, item) FROM stdin;
1	304	15	2
7	451	20	2
\.


--
-- Data for Name: cities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cities (id, name) FROM stdin;
1	Москва
2	Хабаровск
3	Санкт-Петербург
\.


--
-- Data for Name: exam_instance_student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exam_instance_student (student_id, exam_instance_id, cabinet_id, mark) FROM stdin;
24	231	1	12
24	229	1	\N
24	230	7	\N
24	232	7	\N
24	233	1	\N
25	232	7	\N
25	233	1	\N
25	234	7	\N
25	235	1	\N
26	227	7	\N
26	228	1	\N
26	229	7	\N
26	230	1	\N
27	227	7	\N
27	228	1	\N
27	229	7	\N
27	230	1	\N
28	227	7	\N
28	228	1	\N
28	229	7	\N
28	230	1	\N
29	227	7	\N
29	228	1	\N
29	229	7	\N
29	230	1	\N
30	229	7	\N
30	230	1	\N
30	231	7	\N
30	232	1	\N
30	233	7	\N
\.


--
-- Data for Name: exam_instances; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exam_instances (id, max_students, exam_id, profile, date) FROM stdin;
227	20	1	t	2023-05-31
228	20	5	f	2023-05-31
229	20	2	f	2023-05-31
230	20	2	f	2023-05-31
231	20	3	f	2023-05-31
232	20	1	f	2023-05-31
233	20	1	f	2023-05-31
234	20	2	t	2023-05-31
235	20	4	t	2023-05-31
\.


--
-- Data for Name: exams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exams (id, name) FROM stdin;
1	Математика
2	Русский язык
3	Биология
4	Литература
5	Физика
\.


--
-- Data for Name: grade_exam_set; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.grade_exam_set (gradetype_id, exam_id, profile) FROM stdin;
1	1	t
1	5	f
1	2	f
2	2	f
2	3	f
2	1	f
3	1	f
3	2	t
3	4	t
\.


--
-- Data for Name: gradeset; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gradeset (student_id, grade_id) FROM stdin;
24	2
25	3
26	1
27	1
27	3
28	1
28	2
28	3
29	1
29	2
30	2
\.


--
-- Data for Name: gradetypes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gradetypes (id, name) FROM stdin;
1	Физико-математический
2	Химико-биологический
3	Гуманитарный
\.


--
-- Data for Name: languages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.languages (id, name, localname) FROM stdin;
1	Afar	Afaraf                                                                                                                                                                                                                                                         
2	Abkhaz	аҧсуа бызшәа, аҧсшәа                                                                                                                                                                                                                                           
3	Avestan	avesta                                                                                                                                                                                                                                                         
4	Afrikaans	Afrikaans                                                                                                                                                                                                                                                      
5	Akan	Akan                                                                                                                                                                                                                                                           
6	Amharic	አማርኛ                                                                                                                                                                                                                                                           
7	Aragonese	aragonés                                                                                                                                                                                                                                                       
8	Arabic	العربية                                                                                                                                                                                                                                                        
9	Assamese	অসমীয়া                                                                                                                                                                                                                                                        
10	Avaric	авар мацӀ, магӀарул мацӀ                                                                                                                                                                                                                                       
11	Aymara	aymar aru                                                                                                                                                                                                                                                      
12	Azerbaijani	azərbaycan dili                                                                                                                                                                                                                                                
13	South Azerbaijani	تورکجه‎                                                                                                                                                                                                                                                        
14	Bashkir	башҡорт теле                                                                                                                                                                                                                                                   
15	Belarusian	беларуская мова                                                                                                                                                                                                                                                
16	Bulgarian	български език                                                                                                                                                                                                                                                 
17	Bihari	भोजपुरी                                                                                                                                                                                                                                                        
18	Bislama	Bislama                                                                                                                                                                                                                                                        
19	Bambara	bamanankan                                                                                                                                                                                                                                                     
20	Bengali; Bangla	বাংলা                                                                                                                                                                                                                                                          
21	"Tibetan Standard, Tibetan, Central "	བོད་ཡིག                                                                                                                                                                                                                                                        
22	Breton	brezhoneg                                                                                                                                                                                                                                                      
23	Bosnian	bosanski jezik                                                                                                                                                                                                                                                 
24	Catalan; Valencian	català, valencià                                                                                                                                                                                                                                               
25	Chechen	нохчийн мотт                                                                                                                                                                                                                                                   
26	Chamorro	Chamoru                                                                                                                                                                                                                                                        
27	Corsican	corsu, lingua corsa                                                                                                                                                                                                                                            
28	Cree	ᓀᐦᐃᔭᐍᐏᐣ                                                                                                                                                                                                                                                        
29	Czech	čeština, český jazyk                                                                                                                                                                                                                                           
30	Chuvash	чӑваш чӗлхи                                                                                                                                                                                                                                                    
31	Welsh	Cymraeg                                                                                                                                                                                                                                                        
32	Danish	dansk                                                                                                                                                                                                                                                          
33	German	Deutsch                                                                                                                                                                                                                                                        
34	Dzongkha	རྫོང་ཁ                                                                                                                                                                                                                                                         
35	Ewe	Eʋegbe                                                                                                                                                                                                                                                         
36	English	English                                                                                                                                                                                                                                                        
37	Esperanto	Esperanto                                                                                                                                                                                                                                                      
38	Spanish; Castilian	español, castellano                                                                                                                                                                                                                                            
39	Estonian	eesti, eesti keel                                                                                                                                                                                                                                              
40	Basque	euskara, euskera                                                                                                                                                                                                                                               
41	Persian (Farsi)	فارسی                                                                                                                                                                                                                                                          
42	Fula; Fulah; Pulaar; Pular	Fulfulde, Pulaar, Pular                                                                                                                                                                                                                                        
43	Finnish	suomi, suomen kieli                                                                                                                                                                                                                                            
44	Fijian	vosa Vakaviti                                                                                                                                                                                                                                                  
45	Faroese	føroyskt                                                                                                                                                                                                                                                       
46	French	français, langue française                                                                                                                                                                                                                                     
47	Western Frisian	Frysk                                                                                                                                                                                                                                                          
48	Irish	Gaeilge                                                                                                                                                                                                                                                        
49	Scottish Gaelic; Gaelic	Gàidhlig                                                                                                                                                                                                                                                       
50	Galician	galego                                                                                                                                                                                                                                                         
51	Manx	Gaelg, Gailck                                                                                                                                                                                                                                                  
52	Hausa	Hausa, هَوُسَ                                                                                                                                                                                                                                                  
53	Hebrew (modern)	עברית                                                                                                                                                                                                                                                          
54	Hindi	हिन्दी, हिंदी                                                                                                                                                                                                                                                  
55	Hiri Motu	Hiri Motu                                                                                                                                                                                                                                                      
56	Croatian	hrvatski jezik                                                                                                                                                                                                                                                 
57	Haitian; Haitian Creole	Kreyòl ayisyen                                                                                                                                                                                                                                                 
58	Hungarian	magyar                                                                                                                                                                                                                                                         
59	Armenian	Հայերեն                                                                                                                                                                                                                                                        
60	Herero	Otjiherero                                                                                                                                                                                                                                                     
61	Interlingua	Interlingua                                                                                                                                                                                                                                                    
62	Indonesian	Bahasa Indonesia                                                                                                                                                                                                                                               
63	Interlingue	Originally called Occidental; then Interlingue after WWII                                                                                                                                                                                                      
64	Igbo	Asụsụ Igbo                                                                                                                                                                                                                                                     
65	Nuosu	ꆈꌠ꒿ Nuosuhxop                                                                                                                                                                                                                                                  
66	Inupiaq	Iñupiaq, Iñupiatun                                                                                                                                                                                                                                             
67	Ido	Ido                                                                                                                                                                                                                                                            
68	Icelandic	Íslenska                                                                                                                                                                                                                                                       
69	Italian	italiano                                                                                                                                                                                                                                                       
70	Inuktitut	ᐃᓄᒃᑎᑐᑦ                                                                                                                                                                                                                                                         
71	Japanese	日本語 (にほんご)                                                                                                                                                                                                                                                     
72	Javanese	basa Jawa                                                                                                                                                                                                                                                      
73	Georgian	ქართული                                                                                                                                                                                                                                                        
74	Kongo	KiKongo                                                                                                                                                                                                                                                        
75	Kazakh	қазақ тілі                                                                                                                                                                                                                                                     
76	Khmer	ខ្មែរ, ខេមរភាសា, ភាសាខ្មែរ                                                                                                                                                                                                                                     
77	Kannada	ಕನ್ನಡ                                                                                                                                                                                                                                                          
78	Korean	한국어 (韓國語), 조선어 (朝鮮語)                                                                                                                                                                                                                                           
79	Kyrgyz	Кыргызча, Кыргыз тили                                                                                                                                                                                                                                          
80	Latin	latine, lingua latina                                                                                                                                                                                                                                          
81	Ganda	Luganda                                                                                                                                                                                                                                                        
82	Lingala	Lingála                                                                                                                                                                                                                                                        
83	Lao	ພາສາລາວ                                                                                                                                                                                                                                                        
84	Lithuanian	lietuvių kalba                                                                                                                                                                                                                                                 
85	Luba-Katanga	Tshiluba                                                                                                                                                                                                                                                       
86	Latvian	latviešu valoda                                                                                                                                                                                                                                                
87	Malagasy	fiteny malagasy                                                                                                                                                                                                                                                
88	Marshallese	Kajin M̧ajeļ                                                                                                                                                                                                                                                   
89	Māori	te reo Māori                                                                                                                                                                                                                                                   
90	Macedonian	македонски јазик                                                                                                                                                                                                                                               
91	Malayalam	മലയാളം                                                                                                                                                                                                                                                         
92	Mongolian	монгол                                                                                                                                                                                                                                                         
93	Marathi (Marāṭhī)	मराठी                                                                                                                                                                                                                                                          
94	Maltese	Malti                                                                                                                                                                                                                                                          
95	Burmese	ဗမာစာ                                                                                                                                                                                                                                                          
96	Nauru	Ekakairũ Naoero                                                                                                                                                                                                                                                
97	Norwegian Bokmål	Norsk bokmål                                                                                                                                                                                                                                                   
98	North Ndebele	isiNdebele                                                                                                                                                                                                                                                     
99	Nepali	नेपाली                                                                                                                                                                                                                                                         
100	Ndonga	Owambo                                                                                                                                                                                                                                                         
101	Dutch	Nederlands, Vlaams                                                                                                                                                                                                                                             
102	Norwegian Nynorsk	Norsk nynorsk                                                                                                                                                                                                                                                  
103	Norwegian	Norsk                                                                                                                                                                                                                                                          
104	South Ndebele	isiNdebele                                                                                                                                                                                                                                                     
105	Chichewa; Chewa; Nyanja	chiCheŵa, chinyanja                                                                                                                                                                                                                                            
106	Oromo	Afaan Oromoo                                                                                                                                                                                                                                                   
107	Oriya	ଓଡ଼ିଆ                                                                                                                                                                                                                                                          
108	Pāli	पाऴि                                                                                                                                                                                                                                                           
109	Polish	język polski, polszczyzna                                                                                                                                                                                                                                      
110	Portuguese	português                                                                                                                                                                                                                                                      
111	Quechua	Runa Simi, Kichwa                                                                                                                                                                                                                                              
112	Romansh	rumantsch grischun                                                                                                                                                                                                                                             
113	Kirundi	Ikirundi                                                                                                                                                                                                                                                       
114	Romanian	limba română                                                                                                                                                                                                                                                   
115	Russian	русский язык                                                                                                                                                                                                                                                   
116	Kinyarwanda	Ikinyarwanda                                                                                                                                                                                                                                                   
117	Sanskrit (Saṁskṛta)	संस्कृतम्                                                                                                                                                                                                                                                      
118	Sardinian	sardu                                                                                                                                                                                                                                                          
119	Sango	yângâ tî sängö                                                                                                                                                                                                                                                 
120	Slovak	slovenčina, slovenský jazyk                                                                                                                                                                                                                                    
121	Slovene	slovenski jezik, slovenščina                                                                                                                                                                                                                                   
122	Shona	chiShona                                                                                                                                                                                                                                                       
123	Somali	Soomaaliga, af Soomaali                                                                                                                                                                                                                                        
124	Albanian	gjuha shqipe                                                                                                                                                                                                                                                   
125	Serbian	српски језик                                                                                                                                                                                                                                                   
126	Swati	SiSwati                                                                                                                                                                                                                                                        
127	Southern Sotho	Sesotho                                                                                                                                                                                                                                                        
128	Sundanese	Basa Sunda                                                                                                                                                                                                                                                     
129	Swedish	Svenska                                                                                                                                                                                                                                                        
130	Swahili	Kiswahili                                                                                                                                                                                                                                                      
131	Tamil	தமிழ்                                                                                                                                                                                                                                                          
132	Telugu	తెలుగు                                                                                                                                                                                                                                                         
133	Tajik	тоҷикӣ, toğikī, تاجیکی‎                                                                                                                                                                                                                                        
134	Thai	ไทย                                                                                                                                                                                                                                                            
135	Tigrinya	ትግርኛ                                                                                                                                                                                                                                                           
136	Turkmen	Türkmen, Түркмен                                                                                                                                                                                                                                               
137	Tagalog	Wikang Tagalog, ᜏᜒᜃᜅ᜔ ᜆᜄᜎᜓᜄ᜔                                                                                                                                                                                                                                   
138	Tswana	Setswana                                                                                                                                                                                                                                                       
139	Tonga (Tonga Islands)	faka Tonga                                                                                                                                                                                                                                                     
140	Turkish	Türkçe                                                                                                                                                                                                                                                         
141	Tsonga	Xitsonga                                                                                                                                                                                                                                                       
142	Tatar	татар теле, tatar tele                                                                                                                                                                                                                                         
143	Twi	Twi                                                                                                                                                                                                                                                            
144	Tahitian	Reo Tahiti                                                                                                                                                                                                                                                     
145	Ukrainian	українська мова                                                                                                                                                                                                                                                
146	Urdu	اردو                                                                                                                                                                                                                                                           
147	Uzbek	O‘zbek, Ўзбек, أۇزبېك‎                                                                                                                                                                                                                                         
148	Venda	Tshivenḓa                                                                                                                                                                                                                                                      
149	Vietnamese	Tiếng Việt                                                                                                                                                                                                                                                     
150	Volapük	Volapük                                                                                                                                                                                                                                                        
151	Walloon	walon                                                                                                                                                                                                                                                          
152	Wolof	Wollof                                                                                                                                                                                                                                                         
153	Xhosa	isiXhosa                                                                                                                                                                                                                                                       
154	Yiddish	ייִדיש                                                                                                                                                                                                                                                         
155	Yoruba	Yorùbá                                                                                                                                                                                                                                                         
156	Chinese	中文 (Zhōngwén), 汉语, 漢語                                                                                                                                                                                                                                          
157	Zulu	isiZulu                                                                                                                                                                                                                                                        
\.


--
-- Data for Name: languageset; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.languageset (student_id, primary_id, foreign_id) FROM stdin;
24	115	36
25	145	36
26	15	36
27	115	145
28	115	36
29	4	46
30	36	115
\.


--
-- Data for Name: schools; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.schools (id, city_id, name) FROM stdin;
1	1	Школа имени В. И. Вернадского № 1553 
2	2	 Школа № 236 имени Героя Советского Союза Г. И. Щедрина
\.


--
-- Data for Name: student_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student_status (id, name) FROM stdin;
1	Н/А
2	Не зачислен
3	Зачислен
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.students (id, name, school_id, phone, adress, status_id) FROM stdin;
24	Химко Биолог Вальерьевич	1	+1111111111	г. Москва ул. Сталеваров 12	1
25	Гумманитарий Язык Безлогиков	2	+2222222222	п. Медведь-гора ул. Подольская	1
26	Математик Стопроцент Занодович	1	+3333333333	г. Буда ул. Пешт 7	1
27	Каплан Юрий Геннадиевич	1	+444444444	обл. Житомирсксая с. Бурильцево ул. Первомайская д. 95	1
28	Всё Всем Сразович	1	+99999999	г. Москва ул. Арбатская д. 20	1
29	Умумбебве Омзунбебву Осас	1	+7777777777	Нигерия	1
30	Ессс Екк	2	+123213123	ул. Германштруссе	1
\.


--
-- Data for Name: teachers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teachers (id, name, password) FROM stdin;
1	Сергеев Иван Николаевич	12345
\.


--
-- Name: cabinets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cabinets_id_seq', 7, true);


--
-- Name: cities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cities_id_seq', 3, true);


--
-- Name: exam_instances_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exam_instances_id_seq', 235, true);


--
-- Name: exams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exams_id_seq', 5, true);


--
-- Name: gradetypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gradetypes_id_seq', 3, true);


--
-- Name: languages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.languages_id_seq', 157, true);


--
-- Name: schools_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.schools_id_seq', 2, true);


--
-- Name: student_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_status_id_seq', 3, true);


--
-- Name: students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.students_id_seq', 30, true);


--
-- Name: teachers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teachers_id_seq', 1, true);


--
-- Name: cabinets cabinets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cabinets
    ADD CONSTRAINT cabinets_pkey PRIMARY KEY (id);


--
-- Name: cities cities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_pkey PRIMARY KEY (id);


--
-- Name: exam_instances exam_instances_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_instances
    ADD CONSTRAINT exam_instances_pkey PRIMARY KEY (id);


--
-- Name: exams exams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_pkey PRIMARY KEY (id);


--
-- Name: gradetypes gradetypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gradetypes
    ADD CONSTRAINT gradetypes_pkey PRIMARY KEY (id);


--
-- Name: languages languages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_pkey PRIMARY KEY (id);


--
-- Name: schools schools_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools
    ADD CONSTRAINT schools_pkey PRIMARY KEY (id);


--
-- Name: student_status student_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_status
    ADD CONSTRAINT student_status_pkey PRIMARY KEY (id);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (id);


--
-- Name: teachers teachers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (id);


--
-- Name: exam_instance_student exam_instance_student_cabinet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_instance_student
    ADD CONSTRAINT exam_instance_student_cabinet_id_fkey FOREIGN KEY (cabinet_id) REFERENCES public.cabinets(id);


--
-- Name: exam_instance_student exam_instance_student_exam_instance_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_instance_student
    ADD CONSTRAINT exam_instance_student_exam_instance_id_fkey FOREIGN KEY (exam_instance_id) REFERENCES public.exam_instances(id);


--
-- Name: exam_instance_student exam_instance_student_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_instance_student
    ADD CONSTRAINT exam_instance_student_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- Name: exam_instances exam_instances_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_instances
    ADD CONSTRAINT exam_instances_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- Name: grade_exam_set grade_exam_set_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade_exam_set
    ADD CONSTRAINT grade_exam_set_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- Name: grade_exam_set grade_exam_set_gradetype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade_exam_set
    ADD CONSTRAINT grade_exam_set_gradetype_id_fkey FOREIGN KEY (gradetype_id) REFERENCES public.gradetypes(id);


--
-- Name: gradeset gradeset_grade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gradeset
    ADD CONSTRAINT gradeset_grade_id_fkey FOREIGN KEY (grade_id) REFERENCES public.gradetypes(id);


--
-- Name: gradeset gradeset_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gradeset
    ADD CONSTRAINT gradeset_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- Name: languageset languageset_foreign_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languageset
    ADD CONSTRAINT languageset_foreign_id_fkey FOREIGN KEY (foreign_id) REFERENCES public.languages(id);


--
-- Name: languageset languageset_primary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languageset
    ADD CONSTRAINT languageset_primary_id_fkey FOREIGN KEY (primary_id) REFERENCES public.languages(id);


--
-- Name: languageset languageset_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languageset
    ADD CONSTRAINT languageset_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- Name: schools schools_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools
    ADD CONSTRAINT schools_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.cities(id);


--
-- Name: students status_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT status_id FOREIGN KEY (status_id) REFERENCES public.student_status(id);


--
-- Name: students students_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.schools(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO pa;
GRANT ALL ON SCHEMA public TO abituriendadmin;


--
-- Name: TABLE cabinets; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.cabinets TO pa;


--
-- Name: SEQUENCE cabinets_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.cabinets_id_seq TO pa;


--
-- Name: TABLE cities; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.cities TO pa;


--
-- Name: SEQUENCE cities_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.cities_id_seq TO pa;


--
-- Name: TABLE exams; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.exams TO pa;


--
-- Name: SEQUENCE exams_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.exams_id_seq TO pa;


--
-- Name: TABLE gradetypes; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.gradetypes TO pa;


--
-- Name: SEQUENCE gradetypes_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.gradetypes_id_seq TO pa;


--
-- Name: TABLE languages; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.languages TO pa;


--
-- Name: SEQUENCE languages_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.languages_id_seq TO pa;


--
-- Name: TABLE languageset; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.languageset TO pa;


--
-- Name: TABLE schools; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.schools TO pa;


--
-- Name: SEQUENCE schools_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.schools_id_seq TO pa;


--
-- Name: TABLE students; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.students TO pa;


--
-- Name: SEQUENCE students_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.students_id_seq TO pa;


--
-- Name: TABLE teachers; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.teachers TO pa;


--
-- Name: SEQUENCE teachers_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.teachers_id_seq TO pa;


--
-- PostgreSQL database dump complete
--

