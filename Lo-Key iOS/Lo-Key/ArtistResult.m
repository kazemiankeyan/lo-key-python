//
//  ArtistResult.m
//  Lo-Key
//
//  Created by Dilraj Devgun on 6/14/18.
//  Copyright © 2018 Dilraj Devgun. All rights reserved.
//

#import "ArtistResult.h"

@implementation ArtistResult

- (id) initWithName:(NSString *)name andID:(NSString *)ID {
    self = [super init];
    if (self) {
        self.name = name;
        self.artist_id = ID;
    }
    return self;
}

@end
