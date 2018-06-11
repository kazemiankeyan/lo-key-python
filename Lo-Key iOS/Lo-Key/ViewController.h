//
//  ViewController.h
//  Lo-Key
//
//  Created by Dilraj Devgun on 5/10/18.
//  Copyright © 2018 Dilraj Devgun. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "SpotifyClient.h"
#import "SearchResultCellTableViewCell.h"

typedef NS_ENUM(NSInteger, InputFieldLocation) {
    InputFieldLocationDefault,
    InputFieldLocationMiddle,
    InputFieldLocationTop,
};

@interface ViewController : UIViewController <UITextFieldDelegate, UITableViewDataSource, UITableViewDelegate>

@property (weak, nonatomic) IBOutlet UIButton *searchButton;
@property (weak, nonatomic) IBOutlet UITextField *artistInputField;
@property (weak, nonatomic) IBOutlet UIActivityIndicatorView *loadingIndicator;
@property (weak, nonatomic) IBOutlet UITableView *searchResultsTableView;

@end

