from big_o.complexities import ALL_CLASSES

def big_o_report(best, others):
    report = ""
    report += 'Best : {!s:<60s} \n'.format(best)
    for class_, residuals in others.items():
        if type(class_) in ALL_CLASSES:
            report += '{!s:<60s}    (res: {:.2G})\n'.format(class_, residuals)
        else:
            report += '{!s:<60s} {}\n' .format(class_ + ':', residuals)
    return report
