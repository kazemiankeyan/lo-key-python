//
//  ViewController.m
//  Lo-Key
//
//  Created by Dilraj Devgun on 5/10/18.
//  Copyright © 2018 Dilraj Devgun. All rights reserved.
//

#import "ViewController.h"
#import "ArtistResult.h"

@interface ViewController ()

@property (nonatomic) InputFieldLocation inputFieldLocation;
@property (nonatomic) struct spotify_artist_result *search_results;
@property (nonatomic) NSMutableArray *objc_results;
@property (nonatomic) NSUInteger result_size;

@end

@implementation ViewController

@synthesize search_results;
@synthesize result_size;
@synthesize objc_results;

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    result_size = 0;
    self.artistInputField.delegate = self;
    [self.artistInputField addTarget:self action: @selector(textFieldDidChange) forControlEvents:UIControlEventEditingChanged];
    self.searchResultsTableView.dataSource = self;
    self.searchResultsTableView.delegate = self;
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)viewDidLayoutSubviews {
    self.artistInputField.frame = CGRectMake(10, (self.view.frame.size.height/2) - 95, self.view.frame.size.width - 20, 95);
    self.searchButton.frame = CGRectMake(10, self.view.frame.size.height * 0.7, self.view.frame.size.width-20, 40);
    self.searchButton.alpha = 0;
}

- (void)viewDidAppear:(BOOL)animated {
    [self.artistInputField becomeFirstResponder];
}


- (IBAction)didPressSearchButton:(UIButton *)sender {
    NSString *artistName = [self.artistInputField text];
    NSLog(@"%@", artistName);
    [self.artistInputField resignFirstResponder];
    [self moveInputFieldToTopPosition];
    [self getSearchResultsForQuery: artistName];
    
    
    [UIView animateWithDuration:0.5 delay:0 usingSpringWithDamping:0.5 initialSpringVelocity:0.2 options:UIViewAnimationOptionBeginFromCurrentState animations:^{
        self.searchResultsTableView.frame = CGRectMake(0, (self.artistInputField.frame.origin.y + self.artistInputField.frame.size.height) + 20, self.view.frame.size.width, self.view.frame.size.height - ((self.artistInputField.frame.origin.y + self.artistInputField.frame.size.height) + 20));
        self.searchResultsTableView.alpha = 1;
        self.loadingIndicator.alpha = 0;
    } completion:^(BOOL success) {
        [self.searchResultsTableView reloadData];
    }];
}

- (void) getSearchResultsForQuery:(NSString *) query {
    const char *c_query = [query UTF8String];
    int num_results = 0;
    search_results = get_search_results((char *)c_query, (uint32_t)[query length], 10, &num_results);
    
    result_size = num_results;
    NSLog(@"--------------hi-----------------");
    objc_results = [[NSMutableArray alloc] initWithCapacity:num_results];
    struct spotify_artist_result *res_ptr = search_results;
    for (int i = 0; i < num_results; i++) {
        NSString *name = [NSString stringWithUTF8String:(res_ptr + i)->name];
        NSString *ID = [NSString stringWithUTF8String:(res_ptr + i)->artist_id];
        
        ArtistResult *result = [[ArtistResult alloc] initWithName:name andID:ID];
        [objc_results addObject:result];
        NSLog(@"name: %s \nid: %s\n", (res_ptr + i)->name, (res_ptr + i)->artist_id);
    }
    free(search_results);
}

- (void)textFieldDidChange {
    NSString *text = self.artistInputField.text;
    if (text != NULL && [text isEqualToString:@""]) {
        self.artistInputField.placeholder = @"artist name";
        [self putInputFieldInDefaultPosition];
    } else {
        [self putInputFieldInSearchPosition];
    }
}

- (void)moveInputFieldToTopPosition {
    if (self.inputFieldLocation != InputFieldLocationTop) {
        [UIView animateWithDuration:0.7 delay:0 usingSpringWithDamping:0.5 initialSpringVelocity:0.2
                            options:UIViewAnimationOptionBeginFromCurrentState animations:^{
            self.artistInputField.frame = CGRectMake(10, self.view.frame.size.height*0.1, self.view.frame.size.width - 20, 95);
            self.searchButton.frame = CGRectMake(10, (self.view.frame.size.height*0.1) + 95 + 40, self.view.frame.size.width - 20, 40);
            self.searchButton.alpha = 0;
            self.loadingIndicator.alpha = 1;
        } completion:^(BOOL completed) {
            self.inputFieldLocation = InputFieldLocationTop;
        }];
    }
}

- (void)putInputFieldInSearchPosition {
    if (self.inputFieldLocation != InputFieldLocationMiddle) {
        [UIView animateWithDuration:0.3 animations:^{
            self.artistInputField.frame = CGRectMake(10, self.view.frame.size.height/4, self.view.frame.size.width - 20, 95);
            self.searchButton.frame = CGRectMake(10, (self.view.frame.size.height/4) + 95 + 40, self.view.frame.size.width - 20, 40);
            self.searchButton.alpha = 1;
        } completion:^(BOOL completed) {
            self.inputFieldLocation = InputFieldLocationMiddle;
            [self.loadingIndicator startAnimating];
        }];
    }
}

- (void)putInputFieldInDefaultPosition {
    if (self.inputFieldLocation != InputFieldLocationDefault) {
        [UIView animateWithDuration:0.7 delay:0 usingSpringWithDamping:0.5 initialSpringVelocity:0.2
                            options:UIViewAnimationOptionBeginFromCurrentState animations:^{
            self.artistInputField.frame = CGRectMake(10, (self.view.frame.size.height/2) - 95, self.view.frame.size.width - 20, 95);
            self.searchButton.frame = CGRectMake(10, self.view.frame.size.height * 0.7, self.view.frame.size.width - 20, 40);
            self.searchButton.alpha = 0;
        } completion:^(BOOL completed) {
            self.inputFieldLocation = InputFieldLocationDefault;
        }];
    }
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    SearchResultCellTableViewCell *cell = [self.searchResultsTableView dequeueReusableCellWithIdentifier:@"result cell" forIndexPath:indexPath];
    ArtistResult *result = objc_results[indexPath.row];
    NSLog(@"%@\n", result.name);
    [cell setup: result.name];
    return cell;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return result_size;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    
}

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath {
    return 80;
}

@end
