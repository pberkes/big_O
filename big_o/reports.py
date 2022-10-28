from big_o.complexities import ALL_CLASSES

def big_o_report(best, others):
    """ Creates a human-readable report of the output of the big_o function.

    Input:
    ------

    best -- Object representing the complexity class that best fits
            the measured execution times.
    others -- A dictionary of fitted complexity classes to the residuals

    Output:
    -------

    report -- A string describing the report of the big_o function

    """
    report = ""
    report += 'Best : {!s:<60s} \n'.format(best)
    for class_, residuals in others.items():
        if type(class_) in ALL_CLASSES:
            report += '{!s:<60s}    (res: {:.2G})\n'.format(class_, residuals)
        else:
            report += '{!s:<60s} {}\n' .format(class_ + ':', residuals)
    return report
