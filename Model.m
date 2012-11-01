#import "Model.h"

@implementation Car
+(Car*)parse:(id)data
{
	if(!data) return nil;

	Car * model = [[[Car alloc] init] autorelease];
	model.Price = [[data valueForKey:@"price"]    intValue];
	model.Name = [data valueForKey:@"benz"];
	model.Tire = [Tire parse:[data valueForKey:@"tire"]];
	model.Style = [[data valueForKey:@"style"]    intValue];

	return model;
}

+(NSArray*)parses:(id)data
{
    NSMutableArray * list = [NSMutableArray array];
    for(NSDictionary * dic in data)
    {
        Car * model = [Car parse:dic];
        if(model)
             [list addObject:model];
    }
    return list;
}
@end

@implementation Tire
+(Tire*)parse:(id)data
{
	if(!data) return nil;

	Tire * model = [[[Tire alloc] init] autorelease];
	model.Band = [data valueForKey:@"band"];
	model.Weight = [[data valueForKey:@"weight"]    intValue];
	model.Size = [[data valueForKey:@"size"]    intValue];

	return model;
}

+(NSArray*)parses:(id)data
{
    NSMutableArray * list = [NSMutableArray array];
    for(NSDictionary * dic in data)
    {
        Tire * model = [Tire parse:dic];
        if(model)
             [list addObject:model];
    }
    return list;
}
@end

