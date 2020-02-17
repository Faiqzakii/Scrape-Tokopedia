import json
import os
import csv
import datetime

try:
    from TokopediaAPI import(Client, __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from TokopediaAPI import(
        Client, __version__ as client_version)


if __name__ == '__main__':

    print('Client version: {0!s}'.format(client_version))

    _dir = os.getcwd()
    date = datetime.datetime.today().strftime('%d-%B-%Y')
    detail_dir = os.path.join(_dir, 'Detail\\{}'.format(date))

    if not os.path.exists(detail_dir):
        print("creating folder Detail")
        os.makedirs(detail_dir)

    api = Client()
    start = int(input("Start darimana: "))
    end = start + 49999
    path = os.path.join(detail_dir, 'shopid_{}-{}.csv'.format(start, end))

    with open("./prod/products - tokopedia - shopid {} - {}.csv".format(start, end), mode='r', encoding='utf-8') as file:
        products = csv.reader(file, delimiter=';')

        with open(path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['shopid', 'product_id', 'name', 'price', 'desc', 'stock', 'sold', 'txSuccess', 'txReject', 'breadcrumb', 'status', 'condition', 'isKreasiLokal', 'isEligibleCOD', 'isPreOrder', 'view', 'review', 'talk', 'rating', 'url'])

        for product in products:
            try:
                product_id = int(product[1])
            except:
                continue

            try:
                result = api.product_detail(product_id)
            except:
                err_path = os.path.join(detail_dir, 'error-{}.csv'.format(date))

                if not os.path.isfile(err_path):
                    with open(err_path, mode='w', encoding='utf-8', newline='') as error:
                        write = csv.writer(error, delimiter=';')
                        write.writerow(['product_id'])

                with open(err_path, mode='a', encoding='utf-8', newline='') as error:
                    write = csv.writer(error, delimiter=';')
                    write.writerow([product_id])

            try:
                data = result['data']['getPDPInfo']
            except:
                continue

            shopid = data['basic']['shopID']
            name = data['basic']['name']
            price = data['basic']['price']
            desc = data['basic']['description']
            status = data['basic']['status']
            condition = data['basic']['condition']
            breadcrumb = data['category']['breadcrumbURL']
            breadcrumb = breadcrumb[28:len(breadcrumb)]
            txSuccess = data['txStats']['txSuccess']
            txReject = data['txStats']['txReject']
            sold = data['txStats']['itemSold']
            stock = data['stock']['value']
            url = data['basic']['url']
            isKreasiLokal = data['basic']['isKreasiLokal']
            isEligibleCOD = data['basic']['isEligibleCOD']
            isPreOrder = data['preorder']['isActive']
            view = data['stats']['countView']
            review =  data['stats']['countReview']
            talk = data['stats']['countTalk']
            rating = data['stats']['rating']

            with open(path, mode='a', encoding='utf-8', newline='') as writefile:
                writer = csv.writer(writefile, delimiter=';')
                writer.writerow([shopid, product_id, name, price, desc, stock, sold, txSuccess, txReject, breadcrumb, status, condition, isKreasiLokal, isEligibleCOD, isPreOrder, view, review, talk, rating, url])

                print("Berhasil scrape itemid {}".format(product_id))
