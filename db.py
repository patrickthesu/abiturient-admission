import psycopg2
from config import host, user, password, db_name
from datetime import timedelta

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

    def insertExamInstance (self, examid, profile, date, max_students = 20):
        self.cursor.execute (f"INSERT INTO exam_instances (exam_id, profile, max_students, date) VALUES ({examid}, {profile}, {max_students}, '{date}') returning id;")
        self.connection.commit ()
        return self.cursor.fetchone()

    def getRequiredExams (self):
        self.cursor.execute ( "SELECT exam_id, profile  FROM grade_exam_set;" )
        return self.cursor.fetchall()

    def getExamGradetype (self):
        self.cursor.execute ( "SELECT exams.name, exams.id, gradetypes.name, gradetypes.id, profile  FROM grade_exam_set JOIN exams ON exams.id = grade_exam_set.exam_id JOIN gradetypes ON grade_exam_set.gradetype_id=gradetypes.id;" )
        return self.cursor.fetchall()

    def insertExamGradetype (self, examid, gradetypeid, profile):
        self.cursor.execute (f"INSERT INTO grade_exam_set (exam_id, gradetype_id, profile) VALUES ({examid}, {gradetypeid}, {profile});")
        self.connection.commit ()
        return True
    def deleteExamGradetype (self, examid, gradetypeid):
        self.cursor.execute (f"DELETE FROM grade_exam_set WHERE exam_id={examid} and gradetype_id = {gradetypeid};")
        self.connection.commit ()
        return True

    def deleteCabinet (self, cabinetid):
        self.cursor.execute ( f"DELETE FROM cabinets WHERE id = {cabinetid}" )
        self.connection.commit ()
        return True

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
    
    def insertStudent (self, name, school, phone, adress, status = 1):
        self.cursor.execute ( f"INSERT INTO students (name, school_id, phone, adress, status_id) VALUES ('{name}', {school}, '{phone}', '{adress}', {status}) RETURNING id;" )
        self.connection.commit ()
        print ( "Succesfully inserted!" )
        return self.cursor.fetchone()

    def setSucces (self, studentId: int, gradeId: int, success: bool):
        self.cursor.execute ( f"""UPDATE gradeset SET succesfull = {success} WHERE student_id = {studentId} and grade_id = {gradeId};""" )
        self.connection.commit ()
        return True

    def getTeacher ( self, name = "No name", teacher_id = None ):
        if teacher_id != None:
            self.cursor.execute ( f"SELECT * FROM teachers WHERE id = '{teacher_id}';" )
        else:
            self.cursor.execute ( f"SELECT * FROM teachers WHERE name = '{name}';" )
        return self.cursor.fetchall()

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

    def getNotExamedStudents (self):
        self.cursor.execute ( f"SELECT * FROM students WHERE status_id = 1 or status_id = null;" )
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
        self.cursor.execute ( f"""select distinct exams.name, profile, exam_id from exam_instances join exams on exams.id = exam_instances.exam_id;""" ) 
        examList = self.cursor.fetchall()
        out = []

        for i in examList:
            if i [1] == True: out.append ( [str (i[0] + " профильный"), [i[2], i[1]]]) 
            else: out.append ( ( [str (i[0]), [i[2], i[1]]]))


        return out

    def deleteExamInstances (self):
        self.cursor.execute (f"DELETE FROM exam_instances;")
        self.connection.commit ()
        return True

    def deleteExamInstancesStudens (self):
        self.cursor.execute (f"DELETE FROM exam_instance_student;")
        self.connection.commit ()
        return True


    def makeAutoAllExams (self, date):
        self.deleteExamInstancesStudens ()
        self.deleteExamInstances ()

        cabinets = []
        lastCabinetIndex = 0
        for cabinet in self.getCabinets ():
            #print (cabinet[0])
            cabinets.append (cabinet[0])

        examInstances = []
        examSets = []
        for examset in self.getRequiredExams ():
            examInstances.append (self.insertExamInstance ( examset[0], examset[1], date))
            examSets.append (examset)


        for student in self.getNotExamedStudents ():
            print (student[0])
            #students.append (student[0])         
            studExams = self.getExams_ (self.getGradesByStudent (student[0])[0])
            for i in range(len(examSets)):
                for st in studExams:
                    if examSets[i][0] == st[0] and examSets[i][1] == st [1]:
                        self.insertExamInstanceStudent (student[0], examInstances[i][0], cabinets[lastCabinetIndex])
                        #print ( examInstance[i] )
                        lastCabinetIndex += 1
                        if len(cabinets) == lastCabinetIndex: lastCabinetIndex = 0
                        continue

        


    def insertExamInstanceStudent (self, student_id, exam_id, cabinetId):
        self.cursor.execute ( f"INSERT INTO exam_instance_student (student_id, exam_instance_id, cabinet_id) VALUES ('{student_id}', {exam_id}, '{cabinetId}');" )
        self.connection.commit ()
        print ( "Succesfully inserted!" )
        return True

    def getStudentsByGradetype (self, gradetype_id):
        self.cursor.execute (f""" select students.name, students.id from gradeset join students on students.id = gradeset.student_id where grade_id = {gradetype_id} and succesfull is Null;""")
        return self.cursor.fetchall()

    def getExamsCabinetsList ( self, student_id ):
        self.cursor.execute (f"SELECT exams.name, profile, cabinets.name, mark FROM examcabinets INNER JOIN cabinets ON cabinets.id = examcabinets.cabinet_id INNER JOIN exams ON examcabinets.exam_id = exams.id WHERE student_id = {student_id} ;")
        return self.cursor.fetchall()
 
    def getFullGrade ( self, grade_id ):
        self.cursor.execute ( f"""select students.name, students.phone, gradeset.succesfull, exam_instances.exam_id, mark from gradeset join grade_exam_set on gradeset.grade_id = grade_exam_set.gradetype_id join exam_instances on exam_instances.exam_id = grade_exam_set.exam_id join exam_instance_student on exam_instance_student.student_id = gradeset.student_id and exam_instances.id = exam_instance_student.exam_instance_id join students on exam_instance_student.student_id = students.id where grade_id = {grade_id};""");
        studentsList = self.cursor.fetchall ()
        out = []
        currentStudent = ""
        for student in studentsList:
            if student[0] != currentStudent:
                currentStudent = student[0]
                out.append (list(*[student[:3]]))
            if len(out[len(out)-1]) == 6: continue
            out[len(out)-1].append(student[4])

        for i in range(len(out)): 
            out[i].append (round(sum(list(map(lambda x: 0 if x is None else x, out[i][3:])))/3, 2))
        return out

    def getFullExam ( self, exam_id, profile, withId = False):
        if not withId:
            self.cursor.execute (f"SELECT students.name, students.phone, cabinets.name, mark FROM exam_instances FULL JOIN exam_instance_student ON exam_instance_student.exam_instance_id = exam_instances.id FULL JOIN students on students.id = exam_instance_student.student_id FULL JOIN cabinets on cabinets.id = exam_instance_student.cabinet_id where exam_id = {exam_id} and profile = {profile};")
            return self.cursor.fetchall()

        else:
            self.cursor.execute (f"SELECT students.id, students.name, students.phone, cabinets.id, cabinets.name, mark FROM exam_instances FULL JOIN exam_instance_student ON exam_instance_student.exam_instance_id = exam_instances.id FULL JOIN students on students.id = exam_instance_student.student_id FULL JOIN cabinets on cabinets.id = exam_instance_student.cabinet_id where exam_id = {exam_id} and profile = {profile};")
 
            examsList = self.cursor.fetchall()
            dictList = []
            for exam in examsList: 
                dictList.append ({"student_id": exam[0], "student_name": exam[1], "student_phone": exam[2], "cabinet_id": exam[3], "cabinet_name": exam[4], "mark": exam[5]})
            return dictList
     
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


    def setMark ( self, mark, studentId, examId, profile ):
        try:

            self.cursor.execute ( f"SELECT id FROM exam_instances WHERE exam_id = {examId} AND profile = {profile};" )
            exam_instance_id = self.cursor.fetchone ()[0]

            self.cursor.execute ( f"UPDATE exam_instance_student SET mark = {mark} WHERE exam_instance_id = {exam_instance_id} AND student_id = {studentId};" )
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

    def getExamsByGrade (self, gradeId: int):
        self.cursor.execute ( f"""select name, profile from grade_exam_set join exams on exams.id = grade_exam_set.exam_id where gradetype_id = {gradeId};""")

        examList = self.cursor.fetchall()
        out = []
        profile = []

        for exam in examList:
            if not ( exam[0] in out ):
                out.append ( exam[0] )
                if exam[1]: profile.append ( len (out) - 1 )

        for i in profile:
            out[i] += " профильный" 

        return out

    def getStudent ( self, student_id ):
        self.cursor.execute ( f"select * from students where id = {student_id};" )
        return self.cursor.fetchall()

    def getExams (self, gradeList):
        l = ""
        for gradeId in gradeList:
            if gradeId == None: continue
            l += str ( gradeId ) + ","
        
        l = l[:-1]

        self.cursor.execute ( f"""
            SELECT exams.name, profile FROM grade_exam_set 
            JOIN exams ON exams.id = grade_exam_set.exam_id
            WHERE gradetype_id in ({l});
        """ )

        examList = self.cursor.fetchall()
        out = []
        profile = []

        for exam in examList:
            if not ( exam[0] in out ):
                out.append ( exam[0] )
                if exam[1]: profile.append ( len (out) - 1 )

        for i in profile:
            out[i] += " профильный" 

        return out

    def getExams_ (self, gradeList):
        l = ""
        for gradeId in gradeList:
            if gradeId == None: continue
            l += str ( gradeId ) + ","
        
        l = l[:-1]

        self.cursor.execute ( f"""
            SELECT exams.id, profile FROM grade_exam_set 
            JOIN exams ON exams.id = grade_exam_set.exam_id
            WHERE gradetype_id in ({l});
        """ )

        examList = self.cursor.fetchall()
        return examList

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
