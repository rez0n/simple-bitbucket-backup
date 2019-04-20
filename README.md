# simple-bitbucket-backup (API 2.0)
Simple script to backup all repositories and branches from BitBucket to specified folder.
Script use Bitbucket API 2.0 ([API 1.0 will be closed 29 Apr 2019](https://developer.atlassian.com/cloud/bitbucket/deprecation-notice-v1-apis), so many existing scripts will stop work.)

**Usage**

Just edit 11 and 12 line, enter username and password here and add to cron like
```
0 0 * * * python3 /path/to/simple-bitbucket-backup.py >/dev/null 2>&1
```
(Runs every midnight)
And set path to directory to store backups in line 13.

**Requirements**

Only Python 3