frappe.ui.form.on("Company", {
    refresh: function(frm){
        set_gst_field_mandatory_property_nz(frm)
    },
    default_currency: function (frm){
        set_gst_field_mandatory_property_nz(frm)
    }

})

let set_gst_field_mandatory_property_nz = function (frm) {
    if (!frm.is_new() && (frm.doc.default_currency == "NZD" || frm.doc.default_currency == "AUD") ){
            // console.log("=========Inside IFFFF NZ=========")
            frm.set_df_property("custom_default_account_for_gst_collected", "reqd", 1);
            frm.set_df_property("custom_default_account_for_gst_paid", "reqd", 1);
            frm.set_df_property("custom_pt2", "reqd", 1);
            frm.set_df_property("custom_pt1", "reqd", 1);
            frm.set_df_property("custom_pt0", "reqd", 1);
            frm.set_df_property("custom_st2", "reqd", 1);
            frm.set_df_property("custom_st1", "reqd", 1);
            frm.set_df_property("custom_st0", "reqd", 1);
        }
        else{
            // console.log("=========Inside ELSEEE NZ=========")
            frm.set_df_property("custom_default_account_for_gst_collected", "reqd", 0);
            frm.set_df_property("custom_default_account_for_gst_paid", "reqd", 0);
            frm.set_df_property("custom_pt2", "reqd", 0);
            frm.set_df_property("custom_pt1", "reqd", 0);
            frm.set_df_property("custom_pt0", "reqd", 0);
            frm.set_df_property("custom_st2", "reqd", 0);
            frm.set_df_property("custom_st1", "reqd", 0);
            frm.set_df_property("custom_st0", "reqd", 0);
        }
}