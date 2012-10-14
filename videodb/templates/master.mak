<!DOCTYPE html>
<html>
<head>
    ${self.meta()}
    <title>${self.title()}</title>
    
    <!--
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap.min.css')}" />
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap-responsive.min.css')}" />
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
    -->
    
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/reset.css')}" />
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
    
    <script src="${tg.url('/javascript/moo-core.js')}"></script>
    <script src="${tg.url('/javascript/mootools-more-1.4.0.1.js')}"></script>
    
    ${self.resources()}
</head>
<body class="${self.body_class()}">
  <div class="container">
    ${self.main_menu()}
    ${self.body()}
    ${self.footer()}
  </div>
</body>

<%def name="body_class()"></%def>
<%def name="meta()">
  <meta charset="${response.charset}" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</%def>

<%def name="title()">  </%def>
<%def name="resources()"></%def>

<%def name="footer()">
  <!-- FOOTER HERE -->
</%def>

<%def name="main_menu()">
<!-- NAVBAR HERE -->
</%def>

</html>
