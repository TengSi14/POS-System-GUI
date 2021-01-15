from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import HomeWin, QtyWin, payout, inventory
import csv

class MainWindow(QtWidgets.QMainWindow, HomeWin.Ui_HomeWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.qtyDialog = QtyWindow(self)
        self.payoutDialog = PayoutWindow(self)
        self.invDialog = Inventory(self) 
        
        self.items_purchased = {}
        self.next_cnt = 1
        self.tbl_rowCount = 0
        self.item_dict = {}
        self.getInventory()

        self.btn_search.clicked.connect(lambda: self.validate_value(self.lineEdit_search.text()))
        self.btn_next.clicked.connect(lambda:self.next_item(self.lineEdit_sTotal.text()))
        self.btn_discard.clicked.connect(self.discard)
        self.btn_cancel.clicked.connect(self.cancel_purchase)
        self.btn_payout.clicked.connect(self.payout)
        self.view_Inventory.triggered.connect(self.invDialog)



    # ITEMS AVAILABLE ==============================================================================
    def getInventory(self):
        with open('inventory.csv') as invCsv:
            readCSV = csv.reader(invCsv,delimiter=',')
            itm_cnt = 0
            for item in readCSV:
                itm_cnt += 1
                self.item_dict.update({itm_cnt:{'iCode':item[0],'iName':item[1],'iPrice':item[2],'iQty':item[3]}})
        invCsv.close()
        print(self.item_dict)

    # ADD ITEMS ON INVENTORY =======================================================================    
    def addItem(self):
        pass


    def clear_allLineEdit(self):
        self.lineEdit_search.clear()
        self.lineEdit_iCode.clear()
        self.lineEdit_iName.clear()
        self.lineEdit_pQty.clear()
        self.lineEdit_iPrice.clear()
        self.lineEdit_sTotal.clear()  

    # TABLE WIDGET ===(Table Manipulation)================================================================
    def qTbl_update(self):
        tbl_txtList = [self.lineEdit_iCode.text(),self.lineEdit_iName.text(), self.lineEdit_pQty.text(), self.lineEdit_iPrice.text(), self.lineEdit_sTotal.text()]
        tbl_colCount = 0
        
        for text in tbl_txtList:
            self.tableWidget_purchasedItems.setItem(self.tbl_rowCount, tbl_colCount, QtWidgets.QTableWidgetItem(text))
            tbl_colCount += 1
        self.tbl_rowCount += 1
        self.tableWidget_purchasedItems.insertRow(self.tableWidget_purchasedItems.rowCount())

    # SEARCH BUTTON =====================================================================================
    def validate_value(self, item):
        for self.idNum in self.item_dict:
            self.gv_iCode = self.item_dict[self.idNum]['iCode']
            if self.gv_iCode == item:
                self.gv_iName = self.item_dict[self.idNum]['iName']
                self.gv_iPrice = str(self.item_dict[self.idNum]['iPrice']) 
                self.lineEdit_iCode.setText(self.gv_iCode)
                self.lineEdit_iName.setText(self.gv_iName)                
                self.lineEdit_iPrice.setText(self.gv_iPrice)
                self.qtyDialog.show()
                break
            else:
                pass

    # PAYOUT BUTTON =====================================================================================
    def payout(self):
        if self.items_purchased != {}:
            self.payoutDialog.show()
            self.payoutDialog.lineEdit_total.setText(self.lineEdit_total.text())
            self.payoutDialog.lineEdit_cash.textChanged.connect(lambda:self.comp_payout(self.payoutDialog.lineEdit_total.text(), self.payoutDialog.lineEdit_cash.text()))
        else:
            print('no items on the cart')


    def comp_payout(self, comp_total, comp_cash):
        total = int(comp_total)
        cash = int(comp_cash)
        change = str(cash - total)
        self.payoutDialog.lineEdit_change.setText(change)

    # CANCEL BUTTON ======================================================================================
    def cancel_purchase(self):
        if self.items_purchased != {}:
            cancel_msg = QMessageBox(QMessageBox.Warning,'Cancel Purchase','Would you like to cancel the purchases?',
                QMessageBox.Ok|QMessageBox.Cancel)
            cancel_win = cancel_msg.exec_()
            if cancel_win == 1024:
                self.items_purchased = {}  
                self.clear_allLineEdit()
                self.lineEdit_total.clear()
                self.qtyDialog.comp_total = 0
            else:
                pass
        
        else:
            pass

    # DISCARD BUTTON =======================================================================================
    def discard(self):
        if self.lineEdit_iCode.text() != "":
            discard_msg = QMessageBox(
                QMessageBox.Warning,
                'Discard Item',
                'Would you like to remove this item?',
                 QMessageBox.Ok|QMessageBox.Cancel)
            # discard_msg.setWindowTitle('Discard Item')
            # discard_msg.setText('Would you like to remove this item?')
            # discard_msg.setIcon(QMessageBox.Warning)
            #val = discard_msg.StandardButton(QMessageBox.Ok|QMessageBox.Cancel)
            # Ok = 1024, Cancel = 4194304
            discard_win = discard_msg.exec_()
            if discard_win == 1024:
                #deduction of discard Item to Total
                subTotal_val = int(self.lineEdit_sTotal.text())
                total_val = int(self.lineEdit_total.text())
                newTotal = str(total_val - subTotal_val)

                self.lineEdit_total.setText(newTotal)
                self.clear_allLineEdit()
            else:
                pass

        else:
            msg_noItem = QMessageBox()
            msg_noItem.setWindowTitle('')
            msg_noItem.setText('No Item Selected!')
            msg_noItem.setIcon(QMessageBox.Information)

            discard_noItem = msg_noItem.exec_()

    # NEXT BUTTON ================================================================================
    def next_item(self, subTotal):
        self.items_purchased.update({self.next_cnt:{
            'iCode':self.lineEdit_iCode.text(),
            'iName':self.lineEdit_iName.text(),
            'pQty': self.lineEdit_pQty.text(),
            'iPrice':self.lineEdit_iPrice.text(),
            'isubTotal':subTotal
        }})
        
        #deduction of sold product to total qty in item inventory
        sold_qty = self.lineEdit_pQty.text()
        item_qty = self.item_dict[self.idNum]['iQty']
        self.new_iQty = int(item_qty) - int(sold_qty)
        #update item_dict
        self.item_dict[self.idNum]['iQty'] = self.new_iQty
        
        self.next_cnt += 1
        self.qTbl_update()
        self.clear_allLineEdit()
        



class QtyWindow(QtWidgets.QMainWindow, QtyWin.Ui_QtyWindow):

    def __init__(self, parent=None):
        super(QtyWindow, self).__init__(parent)
        self.setupUi(self)
        self.partnerDialog = parent
        self.btn_ok.clicked.connect(self.set_Val_pQty)
        self.comp_total = 0


    def set_Val_pQty(self):
        self.partnerDialog.lineEdit_pQty.setText(self.lineEdit_Qty.text())
        self.compute(self.partnerDialog.lineEdit_iPrice.text(), self.partnerDialog.lineEdit_pQty.text())


    def compute(self, comp_iPrice, comp_pQty):
            try:
                self.hide()
                #for SubTotal
                self.comp_iPrice = int(comp_iPrice)
                self.comp_pQty = int(comp_pQty)
                self.comp_sTotal = self.comp_iPrice * self.comp_pQty
                self.partnerDialog.lineEdit_sTotal.setText(str(self.comp_sTotal))
                #for Total
                self.comp_total += self.comp_sTotal
                self.partnerDialog.lineEdit_total.setText(str(self.comp_total))
            except ValueError:
                #get rid of ValueError caused by empty string from lineEdit pQty and comp_iPrice
                pass 


class PayoutWindow(QtWidgets.QDialog, payout.Ui_PayoutForm):
    def __init__(self, parent=None):
        super(PayoutWindow,self).__init__(parent)
        self.setupUi(self)
        self.partnerDialog = parent


class Inventory(QtWidgets.QDialog, inventory.Ui_Dialog):
    def __init__(self, parent=None):
        super(Inventory, self).__init__(parent)
        self.setupUi(self)
        self.partnerDialog = parent




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

    