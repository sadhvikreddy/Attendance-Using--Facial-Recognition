def gettable(table, date, timein, timeout):
    try:
        x = table + '''<tr>
                        <td>''' + date + '''
                        </td>
                        <td>''' + timein + '''
                        </td>
                        <td>''' + timeout + '''
                        </td></tr>
                        '''
    except TypeError:
        x = x = table + '''<tr>
                        <td>''' + date + '''
                        </td>
                        <td>null
                        </td>
                        <td>null
                        </td></tr>
                        '''
    return x


def endtable(table):
    x = table + '''</table></center></div></center>'''
    return x


def gettable1(table, name, empid, age, gender, contact):
    x = table + '''<tr>
                        <td>''' + name + '''
                        </td>
                        <td>''' + empid + '''
                        </td>
                        <td>''' + age + '''
                        </td>
                        <td>''' + gender + '''
                        </td>
                        <td>''' + contact + '''
                        </td>
                  </tr> '''
    return x
