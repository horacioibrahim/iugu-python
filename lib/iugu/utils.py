"""
Useful for developers purposes
"""

import config, subscriptions, customers, invoices, plans

if config.API_MODE_TEST is not True:
    raise TypeError("::DANGER:: You isn't in mode test. Check your config file")

def loop_remove(objs_list, verbose=0):
    """ Removes all objects of a list returned by getitems()
    """
    for i in objs_list:
        try:
            i.remove()
        except:
            if verbose >= 2:
                print "Not removed due an exception: ", i.id
            else:
                pass

def try_remove(client, verbose=0):
    objs = client.getitems()
    loop_remove(objs, verbose=verbose)
    objs = client.getitems()
    return len(objs)

def try_remove_subs(verbose=0):
     subs = subscriptions.IuguSubscription
     total = try_remove(subs, verbose=verbose)
     if verbose >= 1:
        print "Total of Subscriptions: ", total
     return total

def try_remove_client(verbose=0):
     cvs = customers.IuguCustomer
     total = try_remove(cvs, verbose=verbose)
     if verbose >= 1:
        print "Total of Customers: ", total
     return total

def try_remove_invoices(verbose=0):
    ivs = invoices.IuguInvoice
    total = try_remove(ivs, verbose=verbose)
    if verbose >= 1:
        print "Total of Invoices: ", total
    return total

def try_remove_plans(verbose=0):
    pls = plans.IuguPlan
    total = try_remove(pls, verbose=verbose)
    if verbose >= 1:
        print "Total of Plans: ", total
    return total

def reset_all(tolerance=100, verbose=1):
    """
    Tries to remove all data

    :param tolerance: it's the number of items not deleted because of API's errors

    IMPORTANT: a tolerance very little (e.g. 10) can to cause a loop
    """
    # TODO function ...
    tolerance_limit = tolerance + (tolerance * .20)
    operations_to_remove = [try_remove_plans, try_remove_subs,
                        try_remove_client, try_remove_invoices]
    def _loop_(operation):
        r = tolerance * 2
        while r > tolerance:
            r = operation(verbose=verbose)
            if r > tolerance_limit:
                break

    for op in operations_to_remove:
        _loop_(op)


