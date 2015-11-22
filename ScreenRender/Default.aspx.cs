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
        SetIndexingLabel(false);
    }

    protected void gv1_PageIndexChanged(object source, DataGridPageChangedEventArgs e)
    {
        SetData();
        gv1.DataSource = finalCollection;
        gv1.CurrentPageIndex = e.NewPageIndex;
        gv1.DataBind();
        SetIndexingLabel(true, e.NewPageIndex);
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

    private void SetIndexingLabel(bool IsIndexingPage, int newPageIndex = 0)
    {
        int pageCount = gv1.PageSize;

        if (IsIndexingPage)
        {
            int indexingCount = finalCollection.Count / pageCount;
            if (newPageIndex == indexingCount)
            {
                lblIndex.Text = "Displaying " + ((newPageIndex * pageCount) + 1) + " - " + 
                    (newPageIndex * pageCount + finalCollection.Count() % pageCount).ToString() + " of " + finalCollection.Count() + " records.";
            }
            else
            {
                lblIndex.Text = "Displaying " + ((newPageIndex * pageCount) + 1) + " - " + (newPageIndex * pageCount + pageCount).ToString() + " of " + finalCollection.Count() + " records.";
            }
        }
        else
        {
            gv1.CurrentPageIndex = 0;
            int indexingCount = finalCollection.Count();
            if (indexingCount < pageCount)
            {
                lblIndex.Text = "Displaying " + "1 - " + (0 * pageCount + finalCollection.Count() % pageCount).ToString() + " of " + finalCollection.Count() + " records.";
            }
            else
            {
                lblIndex.Text = "Displaying " + "1 - " + pageCount.ToString() + " of " + finalCollection.Count() + " records.";
            }
        }
    }
}
