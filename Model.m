#import "Model.h"

@implementation Car
+(Car*)parse:(id)data
{
	if(!data) return nil;

	Car * model = [[[Car alloc] init] autorelease];
	model.price = [[data valueForKey:@"price"]    intValue];
	model.style = [[data valueForKey:@"style"]    intValue];
	model.name = [data valueForKey:@"benz"];
	model.tire = [Tire parse:[data valueForKey:@"tire"]];

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

- (void)dealloc
{
    [_benz     release];
    [_tire     release];

    [super dealloc];
}
    
@end

@implementation Tire
+(Tire*)parse:(id)data
{
	if(!data) return nil;

	Tire * model = [[[Tire alloc] init] autorelease];
	model.band = [data valueForKey:@"band"];
	model.weight = [[data valueForKey:@"weight"]    intValue];
	model.size = [[data valueForKey:@"size"]    intValue];

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

- (void)dealloc
{
    [_band     release];

    [super dealloc];
}
    
@end

