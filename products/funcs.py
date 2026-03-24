import requests as req
def updatestockinremoteserver(products, serverip):
    url = f"http://{serverip}/products/updatestockfromthread"
    headers = {'Content-Type': 'application/json'}
    try:
        response = req.post(url, json=products, headers=headers)
        response.raise_for_status()
        return True
    except req.exceptions.RequestException as e:
        print(f"Error updating stock on remote server: {e}")
        return False