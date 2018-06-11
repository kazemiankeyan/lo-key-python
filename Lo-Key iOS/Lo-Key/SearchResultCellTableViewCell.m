//
//  SearchResultCellTableViewCell.m
//  Lo-Key
//
//  Created by Dilraj Devgun on 5/23/18.
//  Copyright © 2018 Dilraj Devgun. All rights reserved.
//

#import "SearchResultCellTableViewCell.h"

@implementation SearchResultCellTableViewCell

- (void)awakeFromNib {
    [super awakeFromNib];
    // Initialization code
}

- (void)setSelected:(BOOL)selected animated:(BOOL)animated {
    [super setSelected:selected animated:animated];
}

- (void)setup:(NSString *)title {
    [self.titleLabel setText:title];
    self.backgroundColor = UIColor.clearColor;
}

@end
