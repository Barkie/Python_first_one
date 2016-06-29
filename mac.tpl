<h1>Full mac list from all devices</h1>
<table>
<tr><th>File name</th><th>Hostname</th><th>Vlan</th><th>Mac Address</th><th>Interface</th><th>Device Vendor</th></tr>
%for row in rows:
    <tr>
    %for col in row:
        <td>{{col}}</td>
    %end
    </tr>
%end
</table>