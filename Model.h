#import <Foundation/Foundation.h>
@class Car;
@class Tire;

@interface Car :NSObject
@property (nonatomic,assign) int  Price;
@property (nonatomic,copy) NSString *  Name;
@property (nonatomic,retain) Tire *  Tire;
@property (nonatomic,assign) int  Style;

+(Car*)parse:(id)data;
+(NSArray*)parses:(id)data;
@end

@interface Tire :NSObject
@property (nonatomic,copy) NSString *  Band;
@property (nonatomic,assign) int  Weight;
@property (nonatomic,assign) int  Size;

+(Tire*)parse:(id)data;
+(NSArray*)parses:(id)data;
@end

