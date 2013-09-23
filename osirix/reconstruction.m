#import "reconstructionFilter.h"

@implementation reconstructionFilter

- (void) initPlugin
{
    NSFileManager *filemgr;
    NSString *currentpath;

    filemgr = [NSFileManager defaultManager];

    currentpath = [filemgr currentDirectoryPath];

    NSLog (@"Current directory is %@", currentpath);

    if ([filemgr changeCurrentDirectoryPath: @"/temp/mydir"] == NO)
        NSLog (@"Cannot change directory.");

    currentpath = [filemgr currentDirectoryPath];

    NSLog (@"Current directory is %@", currentpath);
}





