#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import os
import re
import sys
import time

from playstore.playstore import Playstore


# Default credentials file location.
credentials_default_location = 'credentials.json'

# Default directory where to save the downloaded applications.
downloaded_apk_default_location = 'Downloads'


def get_cmd_args(args: list = None):
    """
    Parse and return the command line parameters needed for the script execution.
    :param args: Optional list of arguments to be parsed (by default sys.argv is used).
    :return: The command line needed parameters.
    """
    parser = argparse.ArgumentParser(description='Download an application (.apk) from the Google Play Store.')
    parser.add_argument('package', type=str, help='The package name of the application to be downloaded, '
                                                  'e.g. "com.spotify.music" or "com.whatsapp"')
    parser.add_argument('-c', '--credentials', type=str, metavar='CREDENTIALS', default=credentials_default_location,
                        help='The path to the JSON configuration file containing the store credentials. By '
                             'default the "credentials.json" file will be used')
    parser.add_argument('-o', '--out', type=str, metavar='FILE', default=downloaded_apk_default_location,
                        help='The path where to save the downloaded .apk file. By default the file will be saved '
                             'in a "Downloads/" directory created where this script is run')
    print(parser.parse_args(args))
    return parser.parse_args(args)


def main():

    args = get_cmd_args()
    package_list_s = ["mac.pocket.mobile.lock.boost.clean.battery.booster", "com.alibaba.aliexpresshd", "com.youdagames.gop3multiplayer", "com.galaxy.gllocker", "com.doubleugames.DoubleUCasino", "com.huuuge.casino.texas", "com.poshmark.app", "mac.magic.magic.clean.october.com", "com.tatemgames.dreamgym", "com.ksmobile.launcher", "com.slicelife.storefront", "com.huuuge.casino.slots", "com.yahoo.mobile.client.android.yahoo", "com.koplagames.kopla01", "com.pixel.gun3d", "com.imvu.mobilecordova", "com.valasmedia.bubblecloudplanet", "air.com.playtika.slotomania", "com.fiverr.fiverr", "com.atari.mobile.rctempire", "com.Kwalee.Tens", "com.yahoo.mobile.client.android.fantasyfootball", "com.tophatter", "com.getheal.patient", "air.com.buffalo_studios.newflashbingo", "net.isitlove.cartercorp.ryan", "com.testm.app", "com.yahoo.mobile.client.android.mail", "com.cheerfulinc.flipagram", "com.speedbooster.optimizer", "com.taggedapp", "com.opera.browser", "com.asiandate", "com.mentormate.android.inboxdollars", "com.dci.magzter", "com.idleif.abyssrium", "myappfreesrl.com.myappfree", "es.socialpoint.DragonCity", "com.tgc.greatcoursesplus", "com.shopkick.app", "com.goodrx", "com.lemonadeinc.lemonade", "com.cmcm.live", "com.bbva.tuyo", "com.contextlogic.wish", "net.slickdeals.android", "air.com.goodgamestudios.empirefourkingdoms", "mac.clean.walle.robot.com"]
    package_list_s2 = ["com.asiandate"]



    try:
        with open("packagename_csv.json", 'r') as loadaff_f:
            load_dict_aff = json.load(loadaff_f)
    except:
        load_dict_aff = []
        pass
    packagename_downed = set(load_dict_aff) & set(package_list_s)
    for del_1 in packagename_downed:
        package_list_s.remove(del_1)
    package_list = set(package_list_s)
    print(package_list,len(package_list))
    for packagename in package_list:
        # time.sleep(60)
        # Make sure to use a valid json file with the credentials.
        api = Playstore(args.credentials.strip(' \'"'))
        try:
            print(packagename)
            # Get the application details.
            app = api.app_details(packagename).docV2
        except AttributeError:
            print('Error when downloading "{0}". Unable to get app\'s details.'.format(packagename))
            continue
            #sys.exit(1)

        details = {
            'package_name': app.docid,
            'title': app.title,
            'creator': app.creator
        }

        if args.out.strip(' \'"') == downloaded_apk_default_location:
            # The downloaded apk will be saved in the Downloads folder (created in the same folder as this script).
            downloaded_apk_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                    downloaded_apk_default_location,
                                                    re.sub('[^\w\-_.\s]', '_', '{0} by {1} - {2}.apk'
                                                           .format(details['title'], details['creator'],
                                                                   details['package_name'])))
        else:
            # The downloaded apk will be saved in the location chosen by the user.
            downloaded_apk_file_path = os.path.abspath(args.out.strip(' \'"'))

        # If it doesn't exist, create the directory where to save the downloaded apk.
        if not os.path.exists(os.path.dirname(downloaded_apk_file_path)):
            os.makedirs(os.path.dirname(downloaded_apk_file_path))

        success = api.download(details['package_name'], downloaded_apk_file_path)

        if not success:
            print('Error when downloading "{0}".'.format(details['package_name']))
            #sys.exit(1)

        dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(dt)
        try:
            with open("packagename_csv.json", 'r') as packagename_f:
                load_dict_package = json.load(packagename_f)
        except:
            load_dict_package = []
            pass

        with open("packagename_csv.json", "w") as f:
            data0 = []
            data0.append(packagename)
            data4 = list(set(data0 + load_dict_package))
            json.dump(data4, f)
            print("加载入文件完成...")
        # with open("down_list.json", "r") as f:
        #     load_dict_aff = json.load(f)
        # with open("down_list.json", "w") as f:
        #     data0 = []
        #     data1 = load_dict_aff + data0.append(packagename)
        #     json.dump(data1, f)
            print("加载入文件完成...")
    print('ok-----------------------------------------------------'*3)

if __name__ == '__main__':
    main()
