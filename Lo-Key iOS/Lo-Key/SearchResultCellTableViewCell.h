//
//  SearchResultCellTableViewCell.h
//  Lo-Key
//
//  Created by Dilraj Devgun on 5/23/18.
//  Copyright © 2018 Dilraj Devgun. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface SearchResultCellTableViewCell : UITableViewCell

@property (weak, nonatomic) IBOutlet UILabel *titleLabel;
- (void)setup:(NSString *) title;

@end
