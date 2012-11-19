import plistlib
import shlex
import sys

def judgeParamStyle(cells):
    if  cmp(cells[0],'int')==0:
        return ["assign","int"]
    elif cmp(cells[0],'bool')==0:
        return ["assign","BOOL"]
    elif cmp(cells[0],'string')==0:
        return ["copy","NSString *"]
    elif cmp(cells[0],'float')==0:
        return ["assign","int"]
    elif cmp(cells[0],'list')==0:
        return ["retain","NSArray *"]
    else:
        return ["retain",cells[1]+" *"]
    

def parseCell(cellword):
        typeInfo    = judgeParamStyle(cellword)
        propertyInfo= "@property (nonatomic,"+typeInfo[0]+") "+typeInfo[1]+" ";
        
        return propertyInfo;

def writeParseMethod(className,implementDict,implementFile):
    
    method_name = "+("+className+"*)parse:(id)data\n{\n"
    judgement   = "\t"+"if(!data) return nil;\n\n"
    createModelInstance = "\t"+className+" * model = [[["+className+" alloc] init] autorelease];\n"
    
    implementFile.write(method_name)
    implementFile.write(judgement)
    implementFile.write(createModelInstance)
    
    for key in implementDict.keys():
        attri   = shlex.split(implementDict[key])
        setence = "\t"+"model."+key+" = "+parseSentenceSuffix(attri)
        implementFile.write(setence)
    
    implementFile.write("\n\t"+"return model;\n")
    implementFile.write("}\n")

def writeParsesMethod(className,implementDict,implementFile):
    parsesMethod="""
+(NSArray*)parses:(id)data
{
    NSMutableArray * list = [NSMutableArray array];
    for(NSDictionary * dic in data)
    {
        """+className+""" * model = ["""+className+""" parse:dic];
        if(model)
             [list addObject:model];
    }
    return list;
}"""
    implementFile.write(parsesMethod+"\n")
    
def parseSentenceSuffix(attri):
    if  cmp(attri[0],'int')==0:
        return "[[data valueForKey:@\""+attri[1]+"\"]    intValue];\n"
    elif cmp(attri[0],'bool')==0:
        return "[[data valueForKey:@\""+attri[1]+"\"]    boolValue];\n"
    elif cmp(attri[0],'string')==0:
        return "[data valueForKey:@\""+attri[1]+"\"];\n"
    elif cmp(attri[0],'float')==0:
        return "[[data valueForKey:@\""+attri[1]+"\"]    floatValue];\n"
    elif cmp(attri[0],'list')==0:
        return "["+attri[1]+" parses:[data valueForKey:@\""+attri[2]+"\"]];\n"
    else:
        return "["+attri[1]+" parse:[data valueForKey:@\""+attri[2]+"\"]];\n"
    
def parseParams(headFile,implementFile,params):
    for key in params.keys():
        value   = params[key]
        splits  = shlex.split(value)
        prefix = parseCell(splits)
        propertys = prefix+" "+key+";\n"
        print propertys
        headFile.write(propertys)

def parseFile(path,Model,wirteType):
    print 'enter parsePlist'
    lib = plistlib.readPlist(path)
    headFile     =open(Model+'.h', wirteType)
    implementFile =open(Model+'.m', wirteType)

    headFile.write("#import <Foundation/Foundation.h>\n")
    implementFile.write("#import \""+Model+".h\"\n\n")

    for key in lib.keys():
        headFile.write("@class "+key+";\n")
    headFile.write("\n");
    for key in lib.keys():
        
        headFile.write("@interface "+key+" :NSObject\n")
        parseParams(headFile,implementFile,lib[key])
        headFile.write("\n+("+key+"*)parse:(id)data;\n")
        headFile.write("+(NSArray*)parses:(id)data;\n")
        headFile.write("@end\n\n")
        
        implementFile.write("@implementation "+key+"\n")
        
        value = lib[key]
        writeParseMethod(key,value,implementFile)
        writeParsesMethod(key,value,implementFile)
        implementFile.write("@end\n\n")
    
    headFile.close()
    implementFile.close()
    
def writeALineTofile(fileName):
    print 'writeing a line to file'

if __name__ == "__main__":
    parseFile(sys.argv[1],sys.argv[2],sys.argv[3])
    
