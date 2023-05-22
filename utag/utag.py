import json
from typing import BinaryIO, Dict


class UTag:
    def __init__(self) -> None:
        self.disease_eng: list = []
        self.disease_persian: list = []
        self.disease_urdu: list = []
        self.disease_urdu_roman: list = []
        self.disease_arabic: list = []
        self.disease_hindi: list = []
        self.disease_description: list = []
        self.symptom_eng: list = []
        self.symptom_persian: list = []
        self.symptom_urdu: list = []
        self.symptom_urdu_roman: list = []
        self.symptom_arabic: list = []
        self.symptom_hindi: list = []
        self.symptom_description: list = []
        self.cause_eng: list = []
        self.cause_persian: list = []
        self.cause_urdu: list = []
        self.cause_urdu_roman: list = []
        self.cause_arabic: list = []
        self.cause_hindi: list = []
        self.cause_description: list = []
        self.principle_of_treatment: list = []
        self.pharmacotherapy: list = []
        self.comp_drug: list = []
        self.reg_theropy: list = []
        self.diet_recom: list = []
        self.diet_restrict: list = []
        self.prevention: list = []
    
    
    def getValueOfKey(self, key: str):
        return self.toDict()[key]
    
    
    def appendTo(self, tag: str, data: str) -> None:
        if tag == 'disease_eng':
            self.disease_eng.append(data)
        elif tag == 'disease_persian':
            self.disease_persian.append(data)
        elif tag == 'disease_urdu':
            self.disease_urdu.append(data)
        elif tag == 'disease_urdu_roman':
            self.disease_urdu_roman.append(data)
        elif tag == 'disease_arabic':
            self.disease_arabic.append(data)
        elif tag == 'disease_hindi':
            self.disease_hindi.append(data)
        elif tag == 'disease_description':
            self.disease_description.append(data)
        elif tag == 'symptom_eng':
            self.symptom_eng.append(data)
        elif tag == 'symptom_persian':
            self.symptom_persian.append(data)
        elif tag == 'symptom_urdu':
            self.symptom_urdu.append(data)
        elif tag == 'symptom_urdu_roman':
            self.symptom_urdu_roman.append(data)
        elif tag == 'symptom_arabic':
            self.symptom_arabic.append(data)
        elif tag == 'symptom_hindi':
            self.symptom_hindi.append(data)
        elif tag == 'symptom_description':
            self.symptom_description.append(data)
        elif tag == 'cause_eng':
            self.cause_eng.append(data)
        elif tag == 'cause_persian':
            self.cause_persian.append(data)
        elif tag == 'cause_urdu':
            self.cause_urdu.append(data)
        elif tag == 'cause_urdu_roman':
            self.cause_urdu_roman.append(data)
        elif tag == 'cause_arabic':
            self.cause_arabic.append(data)
        elif tag == 'cause_hindi':
            self.cause_hindi.append(data)
        elif tag == 'cause_description':
            self.cause_description.append(data)
        elif tag == 'principle_of_treatment':
            self.principle_of_treatment.append(data)
        elif tag == 'pharmacotherapy':
            self.pharmacotherapy.append(data)
        elif tag == 'comp_drug':
            self.comp_drug.append(data)
        elif tag == 'reg_theropy':
            self.reg_theropy.append(data)
        elif tag == 'diet_recom':
            self.diet_recom.append(data)
        elif tag == 'diet_restrict':
            self.diet_restrict.append(data)
        elif tag == 'prevention':
            self.prevention.append(data)
    
    
    def __isOpeningTag(self, line: str) -> bool:
        if line.startswith('<') and line.endswith('>'):
            if line[1] != '/':
                return True
        return False


    def __isClosingTag(self, line: str) -> bool:
        if line.startswith('</') and line.endswith('>'):
            return True
        return False


    def __getCurretTag(self, tag: str) -> str:
        if tag.startswith('</') and tag.endswith('>'):
            return tag[2:-1]
        elif tag.startswith('<') and tag.endswith('>'):
            return tag[1:-1]
        return ""
    
    
    def fromAnnotation(self, lines: list[str]) -> None:
        openingTag = ""
        closingTag = ""
        data = ""

        for line in lines:
            if self.__isOpeningTag(line):
                openingTag = self.__getCurretTag(line)
            elif self.__isClosingTag(line):
                closingTag = self.__getCurretTag(line)
            else:
                data = line
            
            if openingTag and closingTag and data:
                self.appendTo(openingTag, data)
                openingTag = ''
                closingTag = ''
                data = ''

    
    def toDict(self) -> Dict:
        return self.__dict__
    
    
    def fromDict(self, dict: Dict) -> None:
        self.__dict__ = dict
        
    
    def getTags(self) -> list:
        return list(self.__dict__.keys())
    
    
    def saveTags(self, path: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(self.getTags()))



class UTagReader:
    def __init__(self) -> None:
        self.diseases: list = []
    
    
    def getDiseses(self) -> list:
        return self.diseases
    
    
    def __stripLines(self, lines: list[str]) -> list:
        for line in lines:
            line = line.replace('\n', '')
        
        return [line.strip() for line in lines if line]
    
    
    def __findOpeningAndClosingTag(self, lines: list, tag: str) -> tuple:
        openingTag = f'<{tag}>'
        closingTag = f'</{tag}>'
        
        if openingTag in lines and closingTag in lines:
            openingTagLineNum = lines.index(openingTag)
            closingTagLineNum = lines.index(closingTag)
            
            return openingTagLineNum, closingTagLineNum
        return None, None
    
    
    def fromTaggedFile(self, file: BinaryIO) -> None:
        lines = file.readlines()
        lines = [line.decode('utf-8') for line in lines]
        lines = self.__stripLines(lines)
        
        for line in lines:
            if line.startswith('<disease>'):
                openingTagLineNum, closingTagLineNum = self.__findOpeningAndClosingTag(lines, 'disease')
                
                if openingTagLineNum == None or closingTagLineNum == None:
                    continue
                
                disease = UTag()
                disease.fromAnnotation(lines[openingTagLineNum+1:closingTagLineNum])
                self.diseases.append(disease)
                
                lines = lines[closingTagLineNum+1:]
                    
    
    def fromJSONFile(self, diseaseDict: Dict) -> None:
        for disease in diseaseDict['diseases']:
            uTag = UTag()
            uTag.fromDict(disease)
            self.diseases.append(uTag)
                
    
    
    def toJSONFile(self, path: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            diseaseDict: Dict = {
                'diseases': [disease.toDict() for disease in self.diseases]
            }
            
            json.dump(diseaseDict, f, ensure_ascii=False, indent=4)