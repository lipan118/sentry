import {Thread} from 'app/types/events';
import {Event} from 'app/types';
import {StacktraceType} from 'app/types/stacktrace';

import getThreadException from './getThreadException';

// TODO(ts): define raw type
function getThreadStacktrace(thread: Thread, event: Event, raw?: any) {
  const exc = getThreadException(thread, event);
  if (exc) {
    let rv: StacktraceType | undefined = undefined;

    if (!exc.values) {
      return rv;
    }

    for (const singleExc of exc.values) {
      if (singleExc.threadId === thread.id) {
        rv = (raw && singleExc.rawStacktrace) || singleExc.stacktrace;
      }
    }
    return rv;
  }

  if (raw && thread.rawStacktrace) {
    return thread.rawStacktrace;
  }

  if (thread.stacktrace) {
    return thread.stacktrace;
  }

  return undefined;
}

export default getThreadStacktrace;
