from django.contrib import admin

# Register your models here.

from .models import account_info, ledger, investment_info, investment_transaction,cashflow, stock_value
from .models.GL import journal
from .models.sats import sats_source,sats_article

class cashflowAdmin(admin.ModelAdmin):
	#fields = ['year','month','salary','rental','phone','dividendcard','investment','saving']
	fields = ['year']
admin.site.register(cashflow,cashflowAdmin)

class sats_articleAdmin(admin.ModelAdmin):
	fields = ['src','strategy','descr','url','screenshot','validation','start_date','end_date','ror','status','ticker','trend','product','product_type']

admin.site.register(sats_article,sats_articleAdmin)

class account_infoAdmin(admin.ModelAdmin):
    fields = ['identifier','number','company','owner','country','type','status','remark']
    list_display = ('id','identifier','number','company','owner','country','type','status','currency','amount','remark')

admin.site.register(account_info,account_infoAdmin)

class investment_infoAdmin(admin.ModelAdmin):
    list_display = ('identifier','company','country','type','paid_amount','sold_amount','last_update_amount','unit','current_price','current_amount','currency','profit_loss','commission','dividend','total_profit_loss','total_yield','remark')

admin.site.register(investment_info,investment_infoAdmin)

class investment_transactionAdmin(admin.ModelAdmin):
	list_display = ('date','identifier','transaction_type_1','transaction_type_2','price','unit','amount','currency','journal_id','remark')
	
admin.site.register(investment_transaction,investment_transactionAdmin)
'''
class gl_infoAdmin(admin.ModelAdmin):
    list_display = ('id','identifier','balancesheet_type','asset_type','asset_holder','asset_source','level_1_category','level_2_category','remark')

admin.site.register(gl_info,gl_infoAdmin)
'''
class journalAdmin(admin.ModelAdmin):
    list_display = ('id','date','year','month','account','amount','currency','gl_account','balancesheet_type','activity','activity_category','reference')

admin.site.register(journal,journalAdmin)
'''
class parameterAdmin(admin.ModelAdmin):
    list_display = ('value_1','value_2','value_3','value_4','value_5')

admin.site.register(parameter,parameterAdmin)
'''
'''
class account_mAdmin(admin.ModelAdmin):
    list_display = ('date','identifier','amount','currency','monthend_indicator','remark')

admin.site.register(account_me,account_mAdmin)
'''
class ledgerAdmin(admin.ModelAdmin):
    list_display = ('gl_account','account','balancesheet_type','activity','activity_category','amount','currency','remark')

admin.site.register(ledger,ledgerAdmin)

class stockValueAdmin(admin.ModelAdmin):
	#fields = ['year','month','salary','rental','phone','dividendcard','investment','saving']
	fields = ['ticker']
admin.site.register(stock_value,stockValueAdmin)


