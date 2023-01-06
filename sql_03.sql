select
       dtc.BUSINESS_NAME,
       SUM(SALES_VALUE) as total_sale

from data_product_sales dps
inner join data_product dt
on dps.PRODUCT_CODE = dt.PRODUCT_COD
inner join data_store_cad dtc
on  dtc.STORE_CODE = dps.STORE_CODE
where dps.DATE between '2019-01-01' and '2019-03-31'
group by dtc.BUSINESS_NAME
