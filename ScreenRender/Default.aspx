<%@ Page Title="Home Page" Language="C#" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="_Default" %>

<asp:Content ID="BodyContent" ContentPlaceHolderID="MainContent" runat="server">

    <div class="jumbotron">
        <h2>CodeRed SSL Audit</h2>
        <p class="lead">We validate the SSL certificate whether it is getting expired </p>
        <p class="lead">
            From Date:
            <asp:TextBox ID="txtFromDate" runat="server" TextMode="Date"></asp:TextBox>
            To Date:
            <asp:TextBox ID="txtToDate" runat="server"></asp:TextBox>
            <asp:Button ID="btnFind" runat="server" OnClick="btnFind_Click" Text="Find" />
            <asp:DataGrid runat="server" ID="gv1" AutoGenerateColumns="False" CaptionAlign="Top" ViewStateMode="Enabled" AllowPaging="True" OnPageIndexChanged="gv1_PageIndexChanged" BorderStyle="Ridge" PageSize="20">
                <Columns>
                    <asp:BoundColumn HeaderText="URL" DataField="url" />
                    <asp:BoundColumn HeaderText="Expiration Date" DataField="expiration" DataFormatString="{0:MM/dd/yy}" />
                    <asp:BoundColumn HeaderText="SSL Labs Score" DataField="grade" /> 
                    <asp:BoundColumn HeaderText="Has Sha1 Signature" DataField="sha1Signature" />                  
                </Columns>
                <HeaderStyle HorizontalAlign="Center" VerticalAlign="Middle" />
                <ItemStyle HorizontalAlign="Left" VerticalAlign="Top" />
            </asp:DataGrid>
        </p>
        <p class="lead">
            <asp:Label ID="lblIndex" runat="server" Text=""></asp:Label>
        </p>
    </div>
</asp:Content>
