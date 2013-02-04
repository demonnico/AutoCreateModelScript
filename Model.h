#import <Foundation/Foundation.h>
@class Car;
@class Tire;

@interface Car :NSObject
@property (nonatomic,assign) int  price;
@property (nonatomic,assign) int  style;
@property (nonatomic,copy) NSString *  name;
@property (nonatomic,retain) Tire *  tire;

+(Car*)parse:(id)data;
+(NSArray*)parses:(id)data;
@end

@interface Tire :NSObject
@property (nonatomic,copy) NSString *  band;
@property (nonatomic,assign) int  weight;
@property (nonatomic,assign) int  size;

+(Tire*)parse:(id)data;
+(NSArray*)parses:(id)data;
@end

