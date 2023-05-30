import psycopg2
from config import host, user, password, db_name

class Connection ():
    def __init__(self):
        try:
            self.connection = psycopg2.connect (
            host = host,
            user = user,
            password = password,
            database = db_name 
            )
        except Exception as err:
            print (err)

        self.cursor = self.connection.cursor()


    def getCities (self): 
        self.cursor.execute ( "SELECT * FROM cities;" )
        return self.cursor.fetchall()

    def getSchools (self, city_id):
        self.cursor.execute ( f"SELECT id, name FROM schools WHERE city_id = {city_id};" )
        return self.cursor.fetchall()
    
    def getStudentName ( self, student_id ):
        self.cursor.execute ( f"SELECT name FROM students WHERE id = {student_id};" )
        return self.cursor.fetchall()
 
    def getLanguages (self):
        self.cursor.execute ( f"SELECT * FROM languages;" )
        return self.cursor.fetchall()
    
    def insertStudent (self, name, school, phone, adress):
        self.cursor.execute ( f"INSERT INTO students (name, school_id, phone, adress) VALUES ('{name}', {school}, '{phone}', '{adress}') RETURNING id;" )
        self.connection.commit ()
        print ( "Succesfully inserted!" )
        return self.cursor.fetchone()
        # self.cursor.execute ( f"INSERT INTO languageset (name, school_id) VALUES ({name}, {school});" )

        #return self.cursor.fetchall()
    def getTeacher ( self, name = "No name", teacher_id = None ):
        if teacher_id != None:
            self.cursor.execute ( f"SELECT * FROM teachers WHERE id = '{teacher_id}';" )
        else:
            self.cursor.execute ( f"SELECT * FROM teachers WHERE name = '{name}';" )
        return self.cursor.fetchall()

    #def getAllStudentsByExam ( self, examId ):
        
 
    def insertGradeSets ( self, studentId, grades ):
        values = ""
        for grade in grades:
            values += f"({studentId},{grade}),"

        self.cursor.execute ( f"INSERT INTO gradeset (student_id, grade_id) VALUES {values[:-1]};" )
        self.connection.commit ()
        print ( "Succesfully inserted!" )

    def getGradeTypes (self):
        self.cursor.execute ( f"SELECT * FROM gradetypes;" )
        return self.cursor.fetchall()

    def getGradesByStudent ( self, student_id ):
        self.cursor.execute ( f"SELECT grade_id FROM gradeset WHERE student_id = {student_id};" )
        return self.cursor.fetchall()

    def getAllExamsNames (self):
        grades = self.getGradeTypes ()
        gradeIds = []
        for grade in grades:
            gradeIds.append( grade[0] )

        l = ""
        for gradeId in gradeIds:
            l += str ( gradeId ) + ","
        
        l = l[:-1]
        self.cursor.execute ( f"""SELECT DISTINCT name, profile, exam_id FROM examlinks INNER JOIN exams ON exams.id = examlinks.exam_id;""" ) 
        examList = self.cursor.fetchall()
        #print (examList)
        out = []
        #profile = []

        for i in examList:
            if i [1] == True: out.append ( [str (i[0] + " профильный"), [i[2], i[1]]])
            else: out.append ( ( [str (i[0]), [i[2], i[1]]]))


        return out

    def makeAutoAllExams (self):
        self.clearExams ()
        exams = self.getAllExams ()
        cabinets = []
        for cabinet in self.getCabinets ():
            cabinets.append ( cabinet[0] )
        for key in exams:
            self.makeCabinetsExamList ( cabinets, exams[key], key.split(" ")[0], key.split(" ")[1] )

    def getExamsCabinetsList ( self, student_id ):
        self.cursor.execute (f"SELECT exams.name, profile, cabinets.name, mark FROM examcabinets INNER JOIN cabinets ON cabinets.id = examcabinets.cabinet_id INNER JOIN exams ON examcabinets.exam_id = exams.id WHERE student_id = {student_id} ;")
        return self.cursor.fetchall()
 

    def getFullExam ( self, exam_id, profile, withId = False):
        if withId : self.cursor.execute (f"SELECT students.id, students.name, students.phone, students.adress, cabinets.name FROM examcabinets INNER JOIN cabinets ON cabinets.id = examcabinets.cabinet_id INNER JOIN students ON students.id = examcabinets.student_id WHERE exam_id = {exam_id} AND profile = {profile} AND mark IS NULL;")
        else : self.cursor.execute (f"SELECT students.name, students.phone, students.adress, cabinets.name FROM examcabinets INNER JOIN cabinets ON cabinets.id = examcabinets.cabinet_id INNER JOIN students ON students.id = examcabinets.student_id WHERE exam_id = {exam_id} AND profile = {profile} AND mark IS NULL;")
        return self.cursor.fetchall()
     
    def getAllExams (self):
        self.cursor.execute ("SELECT exam_id, profile FROM examlinks;")
        examList = self.cursor.fetchall()
        self.cursor.execute ("SELECT student_id, exam_id, profile FROM gradeset INNER JOIN examlinks ON gradeset.grade_id = examlinks.grade_id;")
        studentExams = self.cursor.fetchall()
        
        sets = {}
        for exam in examList:
            for student in studentExams:
                if [exam[0], exam[1]] == [student[1], student [2]]:
                    try:
                        sets[str ( exam[0] ) + " " + str (exam[1])].append (student[0])
                    except:
                        sets[str ( exam[0] ) + " " + str (exam[1])] = [student[0]]

        for key in sets:
            if key.split(" ")[1] == "False":
                for i in sets[key]:
                    pass
                    #try:
                    #    value2 = sets[( key.split(" ")[0] ) + " " + str (True)]
                    #    for x in range ( len ( value2 )):
                    #        if value2[x] == i:
                    #            del ( sets[( key.split(" ")[0] ) + " " + str (False)][x] )
                    #except:
                    #    pass
        #print (sets)
        return sets 

    #def getExamsCabinets (self):
        #self.cursor.execute ( "select students.name, cabinets.name, exam_id, profile from examcabinets inner join students on examcabinets.student_id = students.id;")
#inner join cabinets on cabinet_id = cabinets.id where exam_id = 1;

    def makeCabinetsExamList ( self, cabinets, examList, exam_id, profile ):

        schools = []
        schoolIds = []

        #print ( examList )

        for studentId in examList:
            schoolId = self.getStudent ( studentId )[0][-1]
            if not ( schoolId in schoolIds ): 
                schoolIds.append ( schoolId ) 
                schools.append ( [[ studentId, schoolId]])
            else:
                for i in range ( len ( schoolIds)):
                    if schoolIds[i] == schoolId:
                        schools[i].append ( [studentId, schoolId] )
                        break

        #print (schoolIds)
        #print (schools)
        #print (exam_id)
        #print (profile)

        #self.cursor.execute ( "select item * itemcount from cabinets;" )
        #maxLengths = self.cursor.fetchall()            

        out = []
        for _ in cabinets:
            out.append ( [] )

        #mostEmptyIndex = 0

        maximalIndex = -1
        for schoolId in range ( len ( schools)):
                if len ( schools [ schoolId ] ) > len ( schools[maximalIndex] ): maximalIndex = schoolId
        
        #print ( cabinets )
        
        while len (cabinets) != 0:
            for cabinetId in range ( len ( cabinets )):
                inserted = False
                if len ( schools ) == 0: break
                for schoolId in range ( len ( schools)):
                    #print ( schoolId )
                    #print ( out[cabinetId][-1][1] )
                    #print (schools[schoolId][1])
                    try:
                        schools[schoolId][-1][0]
                        #print (  )
                    except:
                        pass
                    if len ( schools[schoolId] ) == 0:
                        del ( schools[schoolId] )
                        return
                    if len (out[cabinetId]) == 0:
                        out[cabinetId].append ([schools[schoolId][-1][0],schools[schoolId][-1][1]]) 
                        self.cursor.execute ( f"INSERT INTO examcabinets ( exam_id, profile, student_id, cabinet_id) VALUES ('{exam_id}',{profile},{schools[schoolId][-1][0]},{cabinets[cabinetId]});" )
                        self.connection.commit ()
                        del schools[schoolId][-1]
                        inserted = True
                        break
                    if out[cabinetId][-1][1] != schools[schoolId][-1][1]:
                        out[cabinetId].append ([schools[schoolId][-1][0],schools[schoolId][-1][1]]) 
                        self.cursor.execute ( f"INSERT INTO examcabinets ( exam_id, profile, student_id, cabinet_id) VALUES ('{exam_id}',{profile},{schools[schoolId][-1][0]},{cabinets[cabinetId]});" )
                        self.connection.commit ()  
                        del schools[schoolId][-1]
                        inserted = True
                        break
                if not inserted:
                    for schoolId in range ( len ( schools)):
                        if len ( schools [ schoolId ] ) > len ( schools[maximalIndex] ): maximalIndex = schoolId 
                        out[cabinetId].append ([schools[maximalIndex][-1][0],schools[maximalIndex][-1][1]]) 

                    self.cursor.execute ( f"INSERT INTO examcabinets ( exam_id, profile, student_id, cabinet_id) VALUES ('{exam_id}',{profile},{schools[maximalIndex].pop()[0]},{cabinets[cabinetId]});" )
                    self.connection.commit ()
                    inserted = True
                        
                        #print ("ERROR")
                        #print (err)

            #for schoolId in range ( len ( schools)):

            #for studentId in range ( len ( students )):
                #if len ( students [ studentId ]) 

        
        #for student in students:
        #j    relevant = []
        #   for i in range ( len ( cabinets)):
        #        if len ( out[i] ) - maxLengths[i] > len ( out [mostEmptyIndex] ) - maxLengths[mostEmptyIndex] : mostEmptyIndex = i
        #        if cabinets[i][len(cabinets[i]) - 1][1] == student [1]: continue
        #        relevant.append (i)
        #    if len (relevant) == 0:
        #        out[mostEmptyIndex].append (student)

    def setMark ( self, mark, studentId, examId, profile ):
        try:
            self.cursor.execute ( f"UPDATE examcabinets SET mark = {mark} WHERE exam_id = {examId} AND profile = {profile} AND student_id = {studentId};" )
            self.connection.commit ()
        except Exception as err:
            print (err)

    def checkExistExams ( self ): 
        self.cursor.execute ( f"SELECT * FROM examcabinets;" )
        if len ( self.cursor.fetchall() ) == 0: return False
        return True

    def clearExams ( self ):
        self.cursor.execute ( f"DELETE FROM examcabinets;" )
        self.connection.commit ()

    def getStudent ( self, student_id ):
        self.cursor.execute ( f"select * from students where id = {student_id};" )
        return self.cursor.fetchall()

    def getExams (self, gradeList):
        l = ""
        #print ( gradeList )
        for gradeId in gradeList:
            if gradeId == None: continue
            l += str ( gradeId ) + ","
        
        l = l[:-1]
        self.cursor.execute ( f"""
            SELECT exams.name, profile
            FROM examlinks 
            INNER join exams ON examlinks.exam_id = exams.id
            INNER join gradetypes ON examlinks.grade_id = gradetypes.id
            WHERE grade_id in ({l});
        """ )
        examList = self.cursor.fetchall()
        out = []
        profile = []
        #print (examList)
        for exam in examList:
            if not ( exam[0] in out ):
                out.append ( exam[0] )
                if exam[1]: profile.append ( len (out) - 1 )

        for i in profile:
            out[i] += " профильный" 
        return out

    def getCabinets ( self ):
        self.cursor.execute ( f"SELECT * FROM cabinets;" )
        return self.cursor.fetchall()
    
    def insertCabinet ( self, name, itemcount, item ):
        self.cursor.execute ( f"INSERT INTO cabinets (name, itemcount, item) VALUES ('{name}',{itemcount},{item});" )
        self.connection.commit ()
        print ( "Succesfully inserted!" )

    def insertLanguageSet ( self, student, primary, foreign ):
        self.cursor.execute ( f"INSERT INTO languageset ( student_id, primary_id, foreign_id) VALUES ({student}, {primary}, {foreign});" )
        self.connection.commit ()
        print ( "Succesfully inserted!" )

    def insertLanguage (self, name, localName):
        self.cursor.execute (f"INSERT INTO languages (name, localname) VALUES ('{name}', '{localName}');")
        self.connection.commit ()
        print ( "Succesfully inserted!" )


    def __del__(self):
        if self.connection:
            self.connection.close()
            self.cursor.close()


if __name__ == "__main__":
    c = Connection ()
