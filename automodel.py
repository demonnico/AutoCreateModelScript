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
        return ["retain",cells[0]+" *"]
    

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
        sentence = "\t"+"model."+key+" = "+parseSentenceSuffix(attri)
        implementFile.write(sentence)
    
    implementFile.write("\n\t"+"return model;\n")
    implementFile.write("}\n")

def writeDeallocMethod(className,implementDict,implementFile):
    deallocMethod_header="""
- (void)dealloc
{\n"""

    for key in implementDict.keys():
        attri   = shlex.split(implementDict[key])
        isObj   = judgeIsObjct(attri[0])
        if  isObj==1:
            deallocMethod_header+='    [_'+attri[1]+'     '+'release];\n'
        else:
            print 'its not a object'+attri[0]+attri[1]

    deallocMethod_tail="""
    [super dealloc];
}
    """
    implementFile.write(deallocMethod_header+deallocMethod_tail+"\n");

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
    print "process data:<"+attri[0]+">  <"+attri[1]+">"
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
        return "["+attri[0]+" parse:[data valueForKey:@\""+attri[1]+"\"]];\n"

def judgeIsObjct(obj):
    if cmp(obj,'int')==0 or cmp(obj,'bool')==0 or cmp(obj[0],'float')==0:
        return  0
    else:
        return 1
    
    
def parseParams(headFile,implementFile,params):
    for key in params.keys():
        value   = params[key]
        splits  = shlex.split(value)
        prefix = parseCell(splits)
        propertys = prefix+" "+key+";\n"
        print propertys
        headFile.write(propertys)

def parseFile(path,Model,writeType):
    print 'enter parsePlist'
    lib = plistlib.readPlist(path)
    headFile     =open(Model+'.h', writeType)
    implementFile =open(Model+'.m', writeType)

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
        writeDeallocMethod(key,value,implementFile)
        implementFile.write("@end\n\n")
    
    headFile.close()
    implementFile.close()
    
def writeALineTofile(fileName):
    print 'writeing a line to file'

if __name__ == "__main__":
    parseFile(sys.argv[1],sys.argv[2],sys.argv[3])
    
