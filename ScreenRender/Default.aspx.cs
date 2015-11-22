using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.IO;

public partial class _Default : Page
{
    List<URL> finalCollection;
    protected void Page_Load(object sender, EventArgs e)
    {
        SetData();
    }

   protected void btnFind_Click(object sender, EventArgs e)
    {
        SetData();
        gv1.DataSource = finalCollection;
        gv1.DataBind();
    }

    protected void gv1_PageIndexChanged(object source, DataGridPageChangedEventArgs e)
    {
        SetData();
        gv1.DataSource = finalCollection;
        gv1.CurrentPageIndex = e.NewPageIndex;
        gv1.DataBind();
    }

    private void SetData()
    {
        if (txtToDate.Text.Length > 0 && txtFromDate.Text.Length > 0)
        {
            string json = File.ReadAllText(HttpContext.Current.Server.MapPath(@"outcopy.json"));
            URLCollection resultCollection = JsonConvert.DeserializeObject<URLCollection>(json);
            finalCollection = resultCollection.urls.Where<URL>(i => i.expiration >= Convert.ToDateTime(txtFromDate.Text).Date &&
            i.expiration <= Convert.ToDateTime(txtToDate.Text).Date).ToList<URL>();
        }
    }
}
