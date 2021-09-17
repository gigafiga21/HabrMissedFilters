#!/bin/sh

# Gets regexp by it's name for commit style checking
# Echoes regexp, if preset not exists - echoes `$1`
# Returns 0 if preset with name `$1` exists, 1 if not
# {String} $1 - name of the commit style
function getCommitStyleRegexp {
    STYLE_NAME="${1}";

    case "${STYLE_NAME}" in
        title)
            echo '/^[A-Z].*\.$/p';
            return 0 ;;
        title-issue)
            echo '/^[A-Z].* \(issue \#[0-9]*\)\.$/p';
            return 0 ;;
        conventional)
            echo '/^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([^\n]+\)|)!?:([^\n]*[^.]|[^:]*\n[^\n]*\.)$/p';
            return 0 ;;
        *)
            echo "${STYLE_NAME}";
            return 1 ;;
    esac
}

# Finds safe symbol to substitute newline character for allowing using `\n` in regex
# {String} $1 - string to fins symbol to replace newlines
function getNewlineEscape {
    MESSAGE="$1";
    NL_POSSIBLE=("ζ" "╣");
    NL="";
    LOG="";
    for NL_ITEM in "${NL_POSSIBLE[@]}"; do
        if [[ $MESSAGE != *"$NL_ITEM"* ]]; then
            NL=$NL_ITEM;
            break;
        fi
    done

    # throwing error if no substitution found
    if [[ $NL == "" ]]; then
        return 1;
    fi

    echo "$NL";
    return 0;
}

# Runs regexp testing for commit message
# Echoes "" if commit message does not fit regexp, in other cases string will not be empty
# {String} $1 - commit message
# {String} $2 - regexp for testing
function testCommitStyleRegexp {
    echo -e "$1" | sed -n -E "$2";
}

# Checks git commit naming style
# {String} $1 - commit message to check
# {String} --style - style of the commit
function checkCommitStyle {
    # Initialization
    MESSAGE=$1; shift;
    STYLE_NAME="title";
    while [ -n "$1" ]; do
        case "$1" in
            --style)
                STYLE_NAME=$2;
                shift ;;
        esac
        shift;
    done
    REGEXP=`getCommitStyleRegexp $STYLE_NAME`;

    # Finding safe symbol to substitute newline character for allowing using `\n` in regex
    if [[ $MESSAGE == *"\n"* ]]; then
        NL=`getNewlineEscape "$MESSAGE"`;
        ERROR=$?;

        # Showing error if no newline substitution symbols found
        if [[ $ERROR -ne 0 ]]; then
            printf "\nerror: looks like your commit message contains one of the [${NL_POSSIBLE[*]}] symbols.";
            printf "We use one of them to substitute \`\\n\` in the commit messages to extend regexp abilities.";
            printf "Please, rename your commit somehow.";
            return 2;
        fi
        
        MESSAGE=${MESSAGE//\\n/$NL};
        REGEXP=${REGEXP//\\n/$NL};
    fi

    # Checking commit syntax
    if [[ `testCommitStyleRegexp "$MESSAGE" "$REGEXP"` == "" ]]; then
        printf "\nerror: invalid commit syntax.";
        printf "\n\n  Valid syntax must match regexp ";
        echo $REGEXP;
        printf " \n\n";
        return 1;
    fi

    return 0;
}