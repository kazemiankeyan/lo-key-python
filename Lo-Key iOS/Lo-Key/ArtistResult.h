//
//  ArtistResult.h
//  Lo-Key
//
//  Created by Dilraj Devgun on 6/14/18.
//  Copyright © 2018 Dilraj Devgun. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface ArtistResult:NSObject

@property (nonatomic, strong) NSString *name;
@property (nonatomic, strong) NSString *artist_id;

- (id) initWithName:(NSString *)name andID:(NSString *) ID;

@end
